#!/usr/bin/python3
""" routes that handle all default RestFul API actions for expenses """
from models.expense import Expense
from models import storage
from models.user import User
from models.notification import Notification
from datetime import datetime
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger.utils import swag_from
from models import storage
from flask import jsonify



@app_views.route('/<user_id>/notifications', methods=['GET'], strict_slashes=False)
def get_user_notifications(user_id):
    """ returns notifications beloging to particular user"""
    user = storage.get(User, user_id)
    notification_type = request.args.get('type')
    if user is None:
        abort(404)
    
    notifications = storage.user_all(user_id, Notification)

    notifications_dict = []
    alerts = []
    reminders = []
    achievements = []
    for notification in notifications:
        if notification_type == 'alerts':
            if notification.notification_type == 'alert':
                alerts.append(notification.to_dict())
        elif notification_type == 'achievement':
            if notification.notification_type == 'achievement':
               achievements.append(notification.to_dict())
        elif notification_type  == 'reminder':
            if notification.notification_type == 'reminder':
                reminders.append(notification.to_dict())
        elif notification_type  == 'warning':
            if notification.notification_type == 'warning':
                reminders.append(notification.to_dict())
        else:
            notifications_dict.append(notification.to_dict())
    if notification_type == 'alerts':
        return jsonifiy(alerts), 200
    if notification_type == 'achievements':
        return jsonifiy(achievements), 200
    if notification_type == 'reminders':
        return jsonifiy(reminders), 200
    return jsonify(notifications_dict), 200
@app_views.route('/<user_id>/notifications/<notification_id>', methods=['DELETE'], strict_slashes=False)
def delete_notification(user_id, notification_id):
    """ deletes an notification belonging to particular user id given from storage """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    notification = storage.get(Notification, expense_id)
    if not notification:
        abort(404);
    notification.delete()
    storage.save()
    return jsonify({"success": True}), 201
@app_views.route('/<user_id>/notifications/<notification_id>', methods=['PUT'], strict_slashes=False)
def update_notification(user_id, notification_id):
    """ updates the details of an notification """
    print("===============UPDATE Notification CALLED===============")
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    notification = storage.get(Notification, expense_id)
    if not notification:
        abort(404)
    data = request.get_json()
    data["id"] = notification_id
    data["user_id"] = user_id
    for key, val in data.items():
        if hasattr(notification, key):
            setattr(notification, key, val)
    notification.save()
    return jsonify(notification.to_dict()), 200
