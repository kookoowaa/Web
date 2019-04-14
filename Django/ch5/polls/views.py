from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from polls.models import Question, Choice
#-- logging 추가
import logging
logger = logging.getLogger(__name__)

#-- Class-based GenericView
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """최근 생성된 질문 5개를 반환함"""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


#-- Function-based View
def vote(request, question_id):
    logger.debug("vote().question_id: %s" % question_id)    # logger 추가
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        ## 설문 투표 폼을 다시 보여준다
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You did not select a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        ## POST를 정상적으로 처리하였으면, 항상 리다이렉션 처리
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))