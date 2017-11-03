# Views for admin blueprint
"""
admin/views.py
~~~~~~~~~~~~~~
Script for admin view
"""

#### Libraries
# Standard library
import os

# Local imports
from . import admin
from ..auth import views 
from .forms import CreateBookForm
from .forms import AddAuthorForm, LendRequestForm, ReturnRequestForm
from ..models import Books, Authors, BookPhotos, LendRequest, ReturnRequest
from app import db

# Third-party libraries
from flask import render_template
from flask import request
from flask import flash
from flask import abort
from flask import redirect
from flask import url_for
from flask import send_from_directory
from flask_login import current_user
from flask_login import login_required,login_user, logout_user
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
from flask_paginate import Pagination, get_page_parameter
from flask_paginate import *
from sqlalchemy import update
from werkzeug.utils import secure_filename

@admin.route('/')
@login_required
def adminpage():
    """
    To render admin-base html page 
    """

    if not current_user.is_admin:
        abort(403)

    return render_template('admin-base.html', title='Admin')


@admin.route('/admin-books', methods=['GET', 'POST'])
def admin_books():
    """
    To render admin-books html page
    """

    books = Books.query.all()
    bookphotos = BookPhotos.query.all()

    return render_template('admin-books.html', books=books, bookphotos=bookphotos)



@admin.route('/admin-books/create-book', methods=['GET', 'POST'])
def create_book():
    """
    Renders form template for create book html
    """

    form = CreateBookForm()
  
    if form.validate_on_submit():
        
        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save(os.path.join('media/images/books', filename))

        book = Books(name=form.name.data,
                     author= form.author.data,
                     publication_date=form.publication_date.data,
                     rating=form.rating.data,
                     review=form.review.data,
                     book_count=form.book_count.data)
      
        db.session.add(book)
        db.session.commit()

        bookphotos =BookPhotos(image_name=book.name,
                               path=filename,
                               book_id=book.book_id)
       
        db.session.add(bookphotos) 
        db.session.commit()

        flash('Successfully added book...:')
    
    return render_template('admin-createbook.html', form=form, title='Create Book')


@admin.route('/admin-books/<filename>')
def send_book(filename):
    """
    Function to return book image from directory
    """

    return send_from_directory(os.path.realpath('media/images/books'), filename)


@admin.route('/admin-authors/create-author', methods=['GET', 'POST'])
def create_author():
    """
    Function to render form for create author
    """
    
    form = AddAuthorForm()
    
    if form.validate_on_submit():
        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save(os.path.join('media/images/authors', filename))
      
        author = Authors(author_name=form.author_name.data,
                         place= form.place.data,
                         age=form.age.data,
                         image=filename)

        db.session.add(author)
        db.session.commit()
        flash('Successfully added author...:')
    
    return render_template('admin-createauthor.html', form=form, title='Create Author')


@admin.route('/admin-authors/<filename>')
def send_author(filename):
    """
    Function to return author image from directory
    """
   
    return send_from_directory(os.path.realpath('media/images/authors'), filename)


@admin.route('/admin-authors', methods=['GET', 'POST'])
def admin_authors():
    """
    To render admin-authors html page
    """
    
    authors = Authors.query.all()   

    return render_template('admin-authors.html', authors=authors)






@admin.route('/lend-request', methods=['GET', 'POST'])
def lend_request():
    """
    To render admin-lend html page
    """
    
    lend = LendRequest.query.order_by(LendRequest.lend_id).all()
    books = Books.query.all()

    return render_template('admin-lend.html', lend=lend, books=books)



@admin.route('/lend-request/form', methods=['GET', 'POST'])
def lend_form():
    """
    To render admin-lend html page
    """
    form = LendRequestForm()
    if form.validate_on_submit():
        lend = LendRequest(user_id=form.user_id.data,
                           book_id= form.book_id.data,
                           date=form.date.data,
                           status= form.status.data)

        db.session.add(lend)
        db.session.commit()

        flash('Successfully requested book...:')
    
    return render_template('admin-lendform.html', form=form, title='LendRequest')


@admin.route('/lend-request/lend-approve/<int:lend_id>', methods=['GET', 'POST'])
def lend_approve(lend_id):
    """
    To render admin-lend html page and update status to 'approved'
    """
    
    lend_object = LendRequest.query.get(lend_id)
    lend_object.status = "Approved"

    book_object = Books.query.get(lend_object.book_id)
    book_object.book_count=book_object.book_count-1
    db.session.commit()

    lend = LendRequest.query.order_by(LendRequest.lend_id).all()
    books = Books.query.all()

    return render_template('admin-lend.html' , lend=lend, books=books)


@admin.route('/lend-request/lend-reject/<int:lend_id>', methods=['GET', 'POST'])
def lend_reject(lend_id):
    """
    To render admin-lend html page and update status to 'rejected'
    """

    lend_object = LendRequest.query.get(lend_id)
    lend_object.status = "Rejected"
    book_object = Books.query.get(lend_object.book_id)
    db.session.commit()

    lend = LendRequest.query.order_by(LendRequest.lend_id).all()

    return render_template('admin-lend.html',lend=lend, Books=Books)




@admin.route('/return-request', methods=['GET', 'POST'])
def return_request():
    """
    To render admin-return html page and show return requests
    """

    form = ReturnRequestForm()

    return render_template('admin-return.html')

