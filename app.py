import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, current_user
from your_forms import ChildForm  # Replace with actual import for ChildForm
from your_models import Child, db  # Replace with actual imports for Child and db

app = Flask(__name__)

# Assuming other configurations (e.g., app.config, db.init_app) are above or handled elsewhere

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = YourLoginForm()  # Replace with actual login form
    if form.validate_on_submit():
        # Your login logic here
        pass
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register_child', methods=['GET', 'POST'])
@login_required
def register_child():
    form = ChildForm()
    if form.validate_on_submit():
        if current_user.role == 'superadmin':
            facility_id = current_user.facility_id or 1
        else:
            facility_id = current_user.facility_id
        c = Child(
            mother_name=form.mother_name.data,
            art_number=form.art_number.data,
            village=form.village.data,
            child_name=form.child_name.data,
            dob=form.dob.data,
            facility_id=facility_id
        )
        c.create_tests()
        db.session.add(c)
        db.session.commit()
        flash('Child registered and tests scheduled', 'success')
        return redirect(url_for('index'))
    return render_template('register_child.html', form=form)

@app.route('/child/<int:child_id>', methods=['GET', 'POST'])
@login_required
def view_child(child_id):
    c = Child.query.get_or_404(child_id)
    # Security: facility users can only access own facility
    if current_user.role != 'superadmin' and c.facility_id != current_user.facility_id:
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        # Update test entries
        for t in c.tests:
            done = request.form.get(f'done_{t.id}')
            result = request.form.get(f'result_{t.id}')
            reason = request.form.get(f'reason_{t.id}')
            remarks = request.form.get(f'remarks_{t.id}')
            t.done_date = done if done else None
            t.result = result
            t.reason = reason
            t.remarks = remarks
        db.session.commit()
        flash('Updates saved', 'success')
        return redirect(url_for('view_child', child_id=child_id))
    return render_template('view_child.html', child=c)

if __name__ == '__main__':
    app.run(debug=True)
