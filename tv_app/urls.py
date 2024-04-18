from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('log_in', views.login),

    path('shows', views.tv_shows ),
    path('new', views.add_show_page ),
    path('shows/<int:id>', views.view_a_show ), # go to a show by id
    path('edit_a_show/<int:id>', views.edit_a_show ), # Edit a show by id
    path('update_a_show/<int:id>', views.update_a_show ), # Update a show by id
    path('delete_a_show/<int:id>', views.delete_a_show), # Delete a show by id
    path('delete_a_comment/<int:id>/<int:show_id>', views.delete_a_comment), # Delete a comment by id
    path('add_show', views.get_show ),

    path('logout', views.logout),
    path('post_a_comment/<int:id>' , views.post_a_comment)
]
