import datetime
import os

from bson import ObjectId
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_pymongo import PyMongo

from forms import LevyForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'secret-key'

app.config['MONGO_URI'] = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/levy'
mongo = PyMongo(app)


@app.route('/', methods=['GET', 'POST'])
def create_levy():
    form = LevyForm()
    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "burial_name": form.burial_name.data,
            "amount": form.amount.data,
            "date": datetime.datetime.combine(form.date.data, datetime.time.min),
            "phone_number": form.phone_number.data,
            "arrears": form.arrears.data,
            "signature": form.signature.data,
            "comments": form.comments.data
        }

        mongo.db.levies.insert_one(data)
        flash("Successfully created levy", "success")
        return redirect(url_for('list_levies'))
    return render_template('create.html', form=form)


@app.route('/levies')
def list_levies():
    levies = list(mongo.db.levies.find())
    return render_template('list.html', data=levies)


@app.route('/levies/<levy_id>', methods=['GET', 'POST'])
def get_detail(levy_id):
    levy = mongo.db.levies.find_one({"_id": ObjectId(levy_id)})
    # form = LevyForm()
    if not levy:
        return url_for('not_found')

    if request.method == "POST":
        print(request.form)
        form = LevyForm(request.form, data=levy)
        if form.validate_on_submit():
            data = {
                "name": form.name.data,
                "burial_name": form.burial_name.data,
                "amount": form.amount.data,
                "date": datetime.datetime.combine(form.date.data, datetime.time.min),
                "phone_number": form.phone_number.data,
                "arrears": form.arrears.data,
                "signature": form.signature.data,
                "comments": form.comments.data
            }
            mongo.db.levies.update_one({"_id": ObjectId(levy_id)}, {
                "$set": data
            })

            flash("Successfully edited levy", "success")
            return redirect(url_for('list_levies'))

        else:
            print(form.errors)

    form = LevyForm(data=levy)
    return render_template('edit.html', form=form, name=levy['name'], id=levy['_id'])


@app.route('/delete/<levy_id>', methods=['POST'])
def delete_levy(levy_id):
    levy = mongo.db.levies.find_one({"_id": ObjectId(levy_id)})
    if not levy:
        return url_for('not_found')

    mongo.db.levies.delete_one({"_id": ObjectId(levy_id)})
    flash("Successfully deleted levy", "success")
    return redirect(url_for('list_levies'))


if __name__ == "__main__":
    app.run(debug=True)
