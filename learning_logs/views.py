from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.models import User

# Create your views here.


def index(request):
    """The home page for learning Log."""
    return render(request, 'learning_logs/index.html')


<<<<<<< HEAD
=======
@login_required()
def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def all_topics(request):
    all_topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'all_topics': all_topics}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required()
>>>>>>> ddc47b7
def check_topic_owner(request, topic):
    """Check the owner of the topic whenever required."""
    if topic.owner != request.user:
        raise Http404


def topics(request):
    """Show all topics."""
    # Get public topics
    pub_top = Topic.objects.filter(public=True).order_by('date_added')

    # Get private topics
    if request.user.is_authenticated:
        priv_top = Topic.objects.filter(owner=request.user).order_by('date_added')
        topics = pub_top | priv_top
    else:
        topics = pub_top

    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """Show a single topic and all its entries. """
    topic = get_object_or_404(Topic, id=topic_id)
    # Make sure the topic belongs to the current user.

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required()
def new_topic(request):
    """ Add a new topic. """
    if request.method != 'POST':
        # No data submitted; Create a blank form
        form = TopicForm()
    else:
        # POST data submitted; process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required()
def new_entry(request, topic_id):
    """ Add a new entry for a particular topic. """
    topic = get_object_or_404(id=topic_id)
    check_topic_owner(request, topic)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            if new_entry.topic.owner == request.user:
                new_entry.save()
            else:
                return Http404
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required()
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = get_object_or_404(id=entry_id)
    topic = entry.topic
    # Make sure the topic belongs to the current user.
    check_topic_owner(request, topic)

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
