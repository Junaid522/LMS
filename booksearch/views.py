from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection
from django.contrib.auth import get_user_model
User = get_user_model()

cursor = connection.cursor()


@login_required
def index(request):
	books = ""
	message = ""
	get = True
	user = User.objects.filter(id=request.user.id).first()

	if(request.method == "GET"):
		if('search' in request.GET):
			get = True
			keywords = request.GET['search'].split(',')
			comparision = ""
			for keyword in keywords:
				keyword = keyword.strip()
				keyword = "%" + keyword + "%"
				if(comparision != ""):
					comparision += " AND "
				comparision += "(BkAthr.Isbn LIKE '"+keyword+"' OR BkAthr.Title LIKE '"+keyword+"' OR BkAthr.authors LIKE '"+keyword+"')"

			query = "SELECT BkAthr.Isbn, BkAthr.Title, BkAthr.authors, BkAthr.Availability FROM (SELECT Book.Isbn, Book.Title, GROUP_CONCAT(Authors.Name) authors, Book.Availability FROM Book,Book_Authors,Authors WHERE Book.Isbn = Book_Authors.Isbn AND Book_Authors.Author_id = Authors.Author_id GROUP BY Book.Isbn) AS BkAthr WHERE "+comparision
			cursor.execute(query)
			books = cursor.fetchall()
			try:
				if (user.profile_picture, None):
					image_url = user.profile_picture.url
				return render(request,'booksearch/index.html',{'books':books,'message':"",'get':get, 'image_url': image_url})
			except:
				return render(request, 'booksearch/index.html', {'books': books, 'message': "", 'get': get})
		else:
			try:
				if (user.profile_picture, None):
					image_url = user.profile_picture.url
				return render(request, 'booksearch/index.html', {'books': books, 'message': message, 'get': get, 'image_url':image_url})
			except:
				return render(request, 'booksearch/index.html', {'books': books, 'message': message, 'get': get})
	elif(request.method == "POST"):
		if('cardno' in request.POST):
			keywords = request.POST['cardno'].split(',')
			print(keywords)
			cardno = keywords[0]
			isbn = keywords[1]
			print(cardno,isbn)
			query = "SELECT COUNT(Card_id) FROM Borrower WHERE Card_id = '"+cardno+"' GROUP BY Card_id"
			cursor.execute(query)

			if(cursor.fetchone() != None):
				query = "SELECT COUNT(Loan_id) FROM Book_Loans WHERE Book_Loans.Card_id = '"+str(cardno)+"' AND Book_Loans.Date_in IS NULL GROUP BY Book_Loans.Card_id"
				cursor.execute(query)
				result = cursor.fetchone()
				if(result == None):
					query = "SELECT Book.Availability FROM Book WHERE Book.Isbn = '"+isbn+"'"
					cursor.execute(query)
					availability = cursor.fetchone()
					if(availability[0] == 1):
						query = 'INSERT INTO Book_Loans(Isbn, Card_id, Date_out, Due_date, Date_in) VALUES("'+ isbn +'","'+ str(cardno) +'",CURDATE(),DATE_ADD(Date_out,INTERVAL 14 DAY),NULL)'
						cursor.execute(query)
						query = 'UPDATE Book SET Book.Availability = "0" WHERE Book.isbn = "'+isbn+'"'
						cursor.execute(query)
						message = "Successfully checked out book. Return within 14 days to avoid fine"
					else:
						message = "Book is not available"
				else:
					query = "SELECT Book.Availability FROM Book WHERE Book.Isbn = '"+isbn+"'"
					cursor.execute(query)
					if(result[0] < 3):
						query = 'INSERT INTO Book_Loans(Isbn, Card_id, Date_out, Due_date, Date_in) VALUES("'+ isbn +'","'+ str(cardno) +'",CURDATE(),DATE_ADD(Date_out,INTERVAL 14 DAY),NULL)'
						cursor.execute(query)
						query = 'UPDATE Book SET Book.Availability = "0" WHERE Book.isbn = "'+isbn+'"'
						cursor.execute(query)
						message = "Successfully checked out book. Return within 14 days to avoid fine"
					else:
						message = "Maximum of only 3 books can be checked out"
			else:
				message = "Invalid Card Number."
			try:
				if (user.profile_picture, None):
					image_url = user.profile_picture.url

				return render(request,'booksearch/index.html',{'books':books,'message':message,'get':get, 'image_url': image_url})
			except:
				return render(request, 'booksearch/index.html',
							  {'books': books, 'message': message, 'get': get})
		else:
			print(request.POST)
			try:
				if (user.profile_picture, None):
					image_url = user.profile_picture.url
				return render(request,'booksearch/index.html',{'books':books,'message':message,'get':get, 'image_url': image_url})
			except:
				return render(request, 'booksearch/index.html',
							  {'books': books, 'message': message, 'get': get})



"""

def index(request):
	if(request.method == "POST"):
		isbn = request.POST['search']
		keywords = request.POST['search'].split(',')
		comparision = ""
		for keyword in keywords:
			keyword = "%" + keyword + "%"
			if(comparision != ""):
				comparision += " AND "
			comparision += "(Book.Isbn LIKE '"+keyword+"' OR Book.Title LIKE '"+keyword+"' OR Authors.Name LIKE '"+keyword+"')"
		print(comparision)

		#query = "SELECT Book.Isbn, Book.Title, GROUP_CONCAT(Authors.Name) authors FROM Book,Book_Authors,Authors WHERE (Book.Isbn = Book_Authors.Isbn AND Book_Authors.Author_id = Authors.Author_id) AND ("+comparision+") GROUP BY Book.Isbn"
		query = "SELECT BkAthr.Isbn, BkAthr.Title, BkAthr.authors FROM (SELECT Book.Isbn, Book.Title, GROUP_CONCAT(Authors.Name) authors WHERE Book.Isbn = Book_Authors.Isbn AND Book_Authors.Author_id = Authors.Author_id GROUP BY Book.Isbn) AS BkAthr WHERE "+comparision
		print(query)
		cursor.execute(query)
		books = cursor.fetchall()
		return render(request,'booksearch/index.html',{'books':books})
	else:
		return render(request,'booksearch/index.html',{'books':""})


"""