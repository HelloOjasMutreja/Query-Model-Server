from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Decision, Option, ImageSet, Category, Assist, Tag, HelpfulUpvote, UserDecisionInteraction
from .forms import *
import random
from django.urls import reverse
from django.db.models import Q
import time
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
import inflect
from .recommendations import get_recommendations

def home(request):
    if request.user.is_authenticated:
        decisions = Decision.objects.filter(Q(user=request.user) & Q(is_daily_decision=True))
        context = {'decisions': decisions}
    else:
        context = {}
    return render(request, 'randomizer/home.html', context) 
# end def

@login_required
def recommendations(request):
    user = request.user
    
    # Get new recommendations if available
    new_recommendations = get_recommendations(user)
    
    # Check if new recommendations are available
    if new_recommendations:
        # Update the current list of recommendations in the user's session
        request.session['recommendations'] = [decision.id for decision in new_recommendations]
    else:
        # Get the current list of recommendations from the user's session
        recommendation_ids = request.session.get('recommendations', [])
        new_recommendations = Decision.objects.filter(id__in=recommendation_ids)
    
    context = {'recommended_decisions': new_recommendations}
    return render(request, 'randomizer/recommendations.html', context)
# end def

def feed(request):
    if request.user.is_authenticated:
        # Check if user has recommendations in session
        recommendation_ids = request.session.get('recommendations', [])
        if recommendation_ids:
            decisions = Decision.objects.filter(id__in=recommendation_ids)
        else:
            decisions = Decision.objects.exclude(user=request.user).filter(is_public_decision=True)
    else:
        decisions = Decision.objects.filter(is_public_decision=True)
    
    context = {'decisions': decisions}
    return render(request, 'randomizer/feed.html', context)
# end def

def filter_decisions(request):
    category_ids = request.GET.getlist('category')
    categories = Category.objects.all()
    filtered_decisions = Decision.objects.filter(categories__in=category_ids).distinct()
    context = {
        'decisions': filtered_decisions,
        'categories': categories,
        'selected_categories': category_ids,
    }
    return render(request, 'randomizer/filter_decisions.html', context)
# end def

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    decisions = user.decision_set.all()
    context = {}
    return render(request, 'randomizer/profile.html', context)    
# end def

def capitalize_transform_text(text):
    words = text.split()
    for i, word in enumerate(words):
        if i == 0 or word == 'i':
            words[i] = word.capitalize()
    #   # to small case the text
    #     elif word.isalpha():
    #         words[i] = word.lower()
    return ' '.join(words)
# end def

def quickDecision(request, pk):

    decision = Decision.objects.get(id=pk)
    image_set = decision.image_set
    options = decision.option_set.all()

    if request.method == 'POST':
        # check if the button to toggle daily decision was clicked
        if 'toggle_daily_decision' in request.POST:
            decision.is_daily_decision = not decision.is_daily_decision
            decision.save()
        else:
            # check if option count is less than 4 before adding new option
            if options.count() < 4:
                option = Option.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    decision=decision,
                    content=capitalize_transform_text(request.POST.get('content')),
                )
                # messages.success(request, 'Option added successfully.')
            else:
                messages.error(request, 'Cannot add more than 4 options.')
                return redirect('decision', pk=decision.id)

    context = {'decision': decision, 'options': options}
    return render(request, 'randomizer/quick_decision.html', context)
# end def

def createQuickDecision(request):
    if request.method == 'POST':
        form = DecisionForm(request.POST)
        if form.is_valid():
            decision = form.save(commit=False)
            decision.user = request.user if request.user.is_authenticated else None
            
            if decision.title:
                decision.title = capitalize_transform_text(decision.title)
            else:
                decision.title = str('Untitled Decision')
            
            image_sets = ImageSet.objects.all()
            decision.image_set = mega_random(image_sets) or None
            decision.is_quick_decision = True

            decision.save()

            messages.success(request, 'Decision created successfully!')
            return redirect('quick-decision', pk=decision.pk)
    else:
        form = DecisionForm()

    context = {'form': form}
    return render(request, 'randomizer/quick_create_decision.html', context)
# end def

@login_required(login_url='login')
def updateQuickDecision(request, pk):
    decision = Decision.objects.get(id=pk)

    if decision.is_quick_decision == True:

        if request.user != decision.user:
            messages.error(request, 'You are not allowed here!')
            return redirect('home')

        if request.method == 'POST':
            form = DecisionForm(request.POST, instance=decision)
            if form.is_valid():
                decision = form.save(commit=False)
                decision.title = capitalize_transform_text(decision.title)
                decision.is_quick_decision = True

                decision.save()

                messages.success(request, 'Decision updated successfully!')
                return redirect(quickDecision, pk=decision.id)

            messages.error(request, 'Please correct the errors below.')
        else:
            form = DecisionForm(instance=decision)
    else:
        return redirect('updatePublicDecision')

    context = {'form': form, 'decision': decision}
    return render(request, 'randomizer/quick_update_decision.html', context)
# end def

def savedDecisions(request):
    decisions = Decision.objects.filter(is_quick_decision=True, user=request.user)

    context = {'decisions': decisions}
    return render(request, 'randomizer/saved.html', context)
# end def

def publicDecision(request, pk):
    decision = Decision.objects.get(id=pk)
    image_set = decision.image_set
    assists = Assist.objects.filter(Q(decision=decision) & ~Q(message__isnull=True))
    options = decision.option_set.all()
    situation = decision.situation
    categories = Category.objects.all()

    if request.user.is_authenticated:
        # Create or update the UserDecisionInteraction object for the current user and decision
        user_interaction, created = UserDecisionInteraction.objects.get_or_create(user=request.user, decision=decision)

        # If the user is starting a new interaction, update the start time
        if created or user_interaction.last_interaction_time is None:
            user_interaction.start_timer()

        # Increment the click count for each visit to the public decision page
        user_interaction.click_count += 1
        user_interaction.save()
    else:
        user_interaction = None

    p = inflect.engine()

    if request.method == 'POST':
        if 'select_categories' in request.POST:
            selected_categories = request.POST.getlist('categories', [])
            decision.categories.set(selected_categories)

    # Stop the timer and update the view time when the user leaves the decision page
    if user_interaction and user_interaction.last_interaction_time:
        user_interaction.stop_timer()

    context = {
        'decision': decision,
        'image_set': image_set,
        'options': options,
        'assists': assists,
        'count_in_words': p.number_to_words(len(options)),
        'situation': situation,
        'categories': categories,
    }
    return render(request, 'randomizer/public_decision.html', context)
# end def

def extract_tags_from_title(title):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(title)
    tags = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]
    return tags
# end def

@login_required(login_url='login')
def createPublicDecision(request):
    title = request.POST.get('title', '')
    decision = Decision.objects.create(user=request.user, title=title)
    decision.is_public_decision = True
    decision.is_quick_decision = False
    decision.is_daily_decision = False
    decision.overview = ''
    decision.situation = ''
    decision.save()
    return redirect(updatePublicDecision, pk=decision.id)
# end def

@login_required(login_url='login')
def updatePublicDecision(request, pk):
    decision = Decision.objects.get(id=pk)
    options = decision.option_set.all()
    categories = Category.objects.all()  # Fetch all categories

    if request.user != decision.user:
        messages.error(request, 'You are not allowed here!')
        return redirect('home')

    form = None  # Initialize form to None
    next_step = '1'  # Define a default value for next_step

    if request.method == 'POST': 
        current_step = request.POST.get('step', '1')
        next_step = current_step  # Initialize next_step with the current step

        if current_step == '1':
            form = TitleCategoryForm(request.POST)
            if form.is_valid():
                decision.title = form.cleaned_data['title']
                decision.categories.set(form.cleaned_data['categories'])
                decision.save()

                # Extract tags from the updated title and associate them with the decision
                tags = extract_tags_from_title(decision.title)
                decision.tags.clear()  # Remove existing tags
                for tag_name in tags:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    decision.tags.add(tag)

                # Proceed to the next step
                next_step = '2'
                form = OverviewForm(initial={'overview': decision.overview})  # Pass initial data for the form
            else:
                next_step = '1'  # Stay on the current step in case of errors

        elif current_step == '2':
            if 'back' in request.POST:
                # Go back to step 1
                next_step = '1'
                form = TitleCategoryForm(initial={'title': decision.title, 'categories': decision.categories.all()})  # Pass initial data for the form
            else:
                form = OverviewForm(request.POST)
                if form.is_valid():
                    decision.overview = form.cleaned_data['overview']
                    decision.save()

                    # Proceed to the next step
                    next_step = '3'  # Create a new form for the options
                else:
                    next_step = '2'  # Stay on the current step in case of errors

        elif current_step == '3':
            if 'add_option' in request.POST:
                if options.count() < 4:
                    Option.objects.create(
                        user=request.user if request.user.is_authenticated else None,
                        decision=decision,
                        content=capitalize_transform_text(request.POST.get('content')),
                    )
            elif 'back' in request.POST:
                next_step = '2'
                form = OverviewForm(initial={'overview': decision.overview})
            elif 'advance' in request.POST:
                next_step = '4'
                form = AdditionalFieldsForm(initial={
                    'situation': decision.situation,
                    'contributor_message': decision.contributor_message,
                    'tags': ', '.join(decision.tags.values_list('name', flat=True)),
                })

        # Add the step 4 logic
        if current_step == '4':
            form = AdditionalFieldsForm(request.POST)
            if 'back' in request.POST:
                # Go back to step 3
                next_step = '3'
            elif form.is_valid():
                decision.situation = form.cleaned_data['situation']
                decision.contributor_message = form.cleaned_data['contributor_message']

                # Extract and associate tags with the decision
                tags_input = form.cleaned_data['tags']
                tags = Tag.objects.filter(name__in=tags_input)
                decision.tags.set(tags)

                decision.save()
                messages.success(request, 'Form submitted successfully!')
                return redirect('public-decision', pk=decision.id)
            else:
                next_step = '4'

        # Check if the 'current_step' is in the session
        if 'current_step' in request.session:
            next_step = request.session['current_step']
            del request.session['current_step']

    else:
        form_data = {
            'title': decision.title,
            'categories': decision.categories.first().id if decision.categories.exists() else None,
        }
        form = TitleCategoryForm(initial=form_data)

    context = {'form': form, 'decision': decision, 'step': next_step, 'options': options, 'categories': categories}
    return render(request, 'randomizer/public_update_decision.html', context)
# end def

@login_required(login_url='login')
def deleteDecision(request, pk):
    decision = Decision.objects.get(id=pk)

    if request.user != decision.user:
        messages.warning(request, 'You are not allowed to delete this decision!')
        return redirect('home')
    
    if request.method == 'POST':
        decision.delete()

        messages.success(request, 'Decision deleted successfully!')
        
        return redirect('home')
    
    return render(request, 'randomizer/delete.html', {'obj': decision})
# end def

def deleteOption(request, pk):
    option = Option.objects.get(id=pk)
    decision = option.decision

    option.delete()

    if decision.is_public_decision:
        request.session['current_step'] = '3'  # Set the current step to '3' in the session
        return redirect(updatePublicDecision, pk=decision.id)
    else:
        return redirect(quickDecision, pk=decision.id) 
# end def

def mega_random(objects):

    if objects:
        random_values = []
        for i in range(64):
            random_values.append(random.choice(objects))

        mega_random_value = random.choice(random_values)

        return mega_random_value
    return None
# end def

def randomOption(request, pk):
    decision = Decision.objects.get(id=pk)
    options = decision.option_set.all()
    random_option = mega_random(options)
    random_option_text = random_option.content
    random_option_text = random_option_transform_text(random_option_text)
    context = {'decision': decision, 'random_option': random_option_text}
    return render(request, 'randomizer/random_option.html', context)
# end def

def random_option_transform_text(text):
    words = text.split()
    for i, word in enumerate(words):
        if word.lower() == 'i':
            words[i] = 'you'
        elif word.lower() == 'my':
            words[i] = 'your'
        elif word.lower() == 'mine':
            words[i] = 'yours'
        elif word.lower() == 'me':
            words[i] = 'you'
    return ' '.join(words).capitalize()

def daily_decisions(request):
    decisions = Decision.objects.filter(Q(user=request.user if request.user.is_authenticated else None) & Q(is_daily_decision=True))
    context = {'decisions': decisions}
    return render(request, 'randomizer/daily_decisions.html', context)
# end def

@login_required(login_url='login')
def set_daily_decision(request, pk):
    decision = Decision.objects.get(id=pk)
    decision.is_daily_decision = True
    decision.save()

    messages.success(request, 'Decision set as daily decision!')

    return redirect('quick-decision', pk=decision.id)
# end def

@login_required(login_url='login')
def unset_daily_decision(request, pk):
    decision = Decision.objects.get(id=pk)
    decision.is_daily_decision = False
    decision.save()

    messages.success(request, 'Decision unset as daily decision!')

    return redirect('decision', pk=decision.id)
# end def

def assist_form(request, pk):
    decision = Decision.objects.get(id=pk)
    options = Option.objects.filter(decision=decision)

    if request.method == 'POST':
        option_id = request.POST.get('option')
        message = request.POST.get('message')
        caution = request.POST.get('caution')
        pros = request.POST.get('pros')
        cons = request.POST.get('cons')
        is_anonymous = request.POST.get('anonymous', False)

        assisted_by = request.user if request.user.is_authenticated else None

        if option_id == '':
            option = None
        else:
            option = Option.objects.get(id=option_id)

        if is_anonymous:
            assist = Assist.objects.create(
                decision=decision,
                option=option,
                assisted_by=assisted_by,
                is_anonymous=True,
                message=message,
                caution=caution,
                pros=pros,
                cons=cons
            )
        else:
            assist = Assist.objects.create(
                decision=decision,
                option=option,
                assisted_by=assisted_by,
                message=message,
                caution=caution,
                pros=pros,
                cons=cons
            )

        if decision.contributor_message:
            messages.success(request, decision.contributor_message)
        else:
            messages.success(request, 'Assist created successfully.')

        return redirect(publicDecision, pk=pk)

    context = {'decision': decision, 'options': options}
    return render(request, 'randomizer/assist_form.html', context)
# end def

@login_required(login_url='login')
def upvoteAssist(request, assist_id):
    assist = get_object_or_404(Assist, pk=assist_id)
    
    if request.method == 'POST' and request.user.is_authenticated:
        if request.user == assist.assisted_by:
            messages.error(request, 'You cannot upvote your own assist.')
        else:
            # Check if the user has already upvoted this assist
            if not HelpfulUpvote.objects.filter(assist=assist, user=request.user).exists():
                # Create a new HelpfulUpvote object and increment the helpful count
                HelpfulUpvote.objects.create(assist=assist, user=request.user)
                assist.helpful += 1
                assist.save()
                messages.success(request, 'Assist upvoted successfully.')
            else:
                messages.error(request, 'You have already upvoted this assist.')
    
    return redirect(publicDecision, pk=assist.pk)
# end def

def filter_option_messages(request, pk, option_id):
    decision = Decision.objects.get(id=pk)
    option = Option.objects.get(id=option_id)

    messages = Assist.objects.filter(option=option)
    pros = [vote.pros for vote in messages if vote.pros]
    cons = [vote.cons for vote in messages if vote.cons]

    context = {
        'decision': decision,
        'option': option,
        'messages': messages,
        'pros': pros,
        'cons': cons,
    }
    return render(request, 'randomizer/filter_option_messages.html', context)
# end def