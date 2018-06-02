def updateInstance(request, modelForm, instance):
    if request.method == 'POST':
        form = modelForm(request.POST, instance = instance)
        if form.is_valid():
            instance = form.save()
            instance.save()
    else:
        form = modelForm(instance = instance)
    return form
    

def delete_schoolYear(request, pk='pk'):
    instance = get_object_or_404(School_Year, pk=pk)
    
    return redirect('school-year-list')
    
    
