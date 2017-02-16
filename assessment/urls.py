from django.conf.urls import url
import assessment.views as assessment_views

urlpatterns = [
	url(r'^problem$', assessment_views.problem),
	url(r'^task$', assessment_views.task),
	url(r'^get_task$', assessment_views.get_task),	
	url(r'^add_assessor$', assessment_views.add_assessor),	
	url(r'^delete_assessor$', assessment_views.delete_assessor),	
	url(r'^get_results$', assessment_views.get_results),
	url(r'^instructions$', assessment_views.instructions),
]