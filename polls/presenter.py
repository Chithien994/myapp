from .models import Question


DELETE 	= "delete"
SAVE	= "save"

class PollsPresenter():
	def add(request):
		question_text = request.POST.get('question_key','')
		if question_text:
			Question.create_question(question_text)

	def options(request):
		option = request.POST.get('option','');
		if option.lower() == DELETE:
			Question.delete_question(request.POST.getlist('id_list'))
			return
		if option.lower() == SAVE:
			try:
				id = int(request.POST.get('question_id',''))
				question_text = request.POST.get('question_text','')
				time = request.POST.get('date_time_0','')+" "+request.POST.get('date_time_1','')
				Question.update_question(id, question_text, time)
			except Exception as e:
				return
			return	


	def ordering(request):
		ordering = request.GET.get('ordering')
		if ordering == 'pub_date':
			return 'pub_date'
		return '-pub_date'
		

	def count(request):
		try:
			count = int(request.GET.get('count'))
			if count > 0:
				return count
			return Question.getCount()
		except Exception as e:
			return Question.getCount()
		


		