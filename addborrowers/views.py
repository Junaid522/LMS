from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection
from .models import Borrower
from django.contrib.auth import get_user_model
User = get_user_model()

cursor = connection.cursor()

@login_required
def index(request):
	ssnexist = False
	message = ""
	user = User.objects.filter(id=request.user.id).first()
	if(request.method == "POST"):
		fname = request.POST['fname']
		ssn = request.POST['ssn']
		address = request.POST['address']
		phone = request.POST['phone']

		query = "SELECT Ssn FROM Borrower WHERE Ssn = '" + ssn + "'"
		cursor.execute(query)

		if(cursor.fetchone() != None):
			ssnexist = True
		else:
			query = 'INSERT INTO Borrower(Ssn,Bname,Address,Phone) VALUES("'+ ssn +'","'+ fname +'","'+ address +'","'+ phone +'");'
			cursor.execute(query)
			message = "Successfully added the borrower"
	try:
		if (user.profile_picture, None):
			image_url = user.profile_picture.url
		return render(request,'addborrowers/index.html',{'ssnexist':ssnexist,'message':message, 'image_url': image_url})
	except:
		return render(request, 'addborrowers/index.html',
					  {'ssnexist': ssnexist, 'message': message})