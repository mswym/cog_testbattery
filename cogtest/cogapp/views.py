from django.shortcuts import render, redirect, HttpResponse


# Create your views here.
def cognitive_assessment_home(request):
    """
    This view is the controller for the all activity. It checks the current status of the pre/post test.
    5 possibilities:
    1) This is the first activity for the participant:
        - Create a task stack (random)
        - Update status (pre/post - phase1)
        - Launch the first activity
    2) There is an another activity in the task stack:
        - Save last activity results
        - Launch the next activity
    3) This is the break
        - Save last activity results
        - Exit this view and call to 'end-task' view
    4) This is the first activity after the break:
        - Do not save last activity results
        - Update status (pre/post - phase2)
        - Launch activity on task stack
    5) No more activity on task stack:
        - Save last activity results
        - Update status (pre -> post OR end)
        - Call to exit view 'end_task'
    """
    participant = ParticipantProfile.objects.get(user=request.user.id)
    # Check if participant is doing the test for the first time:
    if 'cognitive_tests_status' not in participant.extra_json:
        init_participant_extra_json(participant)
    add_participant_timestamp(participant)
    # task index is updated when the last task has been completed
    idx_task = participant.extra_json['cognitive_tests_current_task_idx']
    # Get current task context and name according to task idx:
    current_task_object = get_current_task_context(participant, idx_task)
    # 3 use cases: play / time for break / time to stop
    if current_task_object is not None and not participant.extra_json['cognitive_tests_break']:
        return launch_task(request, participant, current_task_object, idx_task)
    elif current_task_object is not None:
        return exit_for_break(participant)
    else:
        return end_task(participant)

def cognitive_task(request):
    """
        View used to render all activities in the pre/post assessment
        Render a base html file that uses a custom filter django tag to include the correct js scripts
    """
    participant = ParticipantProfile.objects.get(user=request.user.id)
    screen_params = Answer.objects.get(participant=participant, question__handle='prof-mot-1').value
    current_task_idx = participant.extra_json["cognitive_tests_current_task_idx"]
    stack_tasks = participant.extra_json["cognitive_tests_task_stack"]
    current_task = f"{stack_tasks[current_task_idx]}"
    return render(request,
                  'base_pre_post_app.html',
                  {"CONTEXT": {"screen_params": screen_params, "task": current_task}})


def exit_view_cognitive_task(request):
    participant = ParticipantProfile.objects.get(user=request.user.id)
    idx_task = participant.extra_json['cognitive_tests_current_task_idx']
    # If the participant has just played, store results of last tasks:
    if store_previous_task(request, participant, idx_task):
        # Update task index for next visit to the view
        update_task_index(participant)
    return redirect(reverse(cognitive_assessment_home))