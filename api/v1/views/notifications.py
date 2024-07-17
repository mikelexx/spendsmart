#!/usr/bin/python3
""" routes that handle all default RestFul API actions for notifications """
from models import storage
from models.user import User
from models.collection import Collection
from models.notification import Notification
from datetime import datetime
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger.utils import swag_from
from models import storage
from flask import jsonify

@app_views.route('/notifications',
                 methods=['POST'],
                 strict_slashes=False)
def post_notifications():
    data  = request.get_json()
    message = data.get('message')
    for key in data:
        if key not in ['message', 'notification_type', 'user_id', 'collection_id']:
            abort(400, 'unrecognized field {}'.format(key))
    if not message:
        abort(400, description='must provide a message')
    elif type(message) is not str:
        abort(400, description='ony string types allowed for message')
    for val in ['collection_id', 'user_id', 'notification_type']:
        field = data.get(val)
        if not field:
            abort(400, description='missing {}'.format(val))
        elif not isinstance(field, str):
            abort(400, description='invalid {}'.format(val))
        elif len(field) == 0:
            abort(400, description='empty {} not allowed'.format(val))
        else:
            if val == 'collection_id':
                collection = storage.get(Collection, field)
                if not collection:
                    abort(400, description='collection id specified does not exist')
            if val == 'user_id':
                user  = storage.get(User, field)
                if not user:
                    abort(400, description='user id specified does not exist')
    notif = Notification(**data)
    notif.save()
    return jsonify(notif.to_dict()), 201

@app_views.route('/users/<user_id>/notifications',
                 methods=['GET'],
                 strict_slashes=False)
def get_user_notifications(user_id):
    """ returns notifications beloging to particular user"""
    user = storage.get(User, user_id)
    sort = request.args.get("sort")
    reverse = False
    read = request.args.get('read')
    if sort and sort == 'descending':
        reverse = True
    is_read = False
    if read and isinstance(read, bool):
        is_read = read
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
        elif notification_type == 'reminder':
            if notification.notification_type == 'reminder':
                reminders.append(notification.to_dict())
        elif notification_type == 'warning':
            if notification.notification_type == 'warning':
                reminders.append(notification.to_dict())
        else:
            notifications_dict.append(notification.to_dict())
    if notification_type == 'alerts':
        if read is not None:
            alerts = [
                alert for alert in alerts if alert.get('is_read') is is_read
            ]
        return jsonifiy(alerts), 200
    if notification_type == 'achievements':
        if read is not None:
            achievements = [
                ach for ach in achievements if ach.get('is_read') is is_read
            ]
        return jsonifiy(achievements), 200
    if notification_type == 'reminders':
        if read is not None:
            reminders = [
                rem for rem in reminders if rem.get('is_read') is is_read
            ]
        return jsonifiy(reminders), 200
    sorted_notifications = sorted(notifications_dict,
                                  key=lambda x: x['created_at'],
                                  reverse=reverse)
    if read is not None:
        sorted_notifications = [
            notif for notif in sorted_notifications
            if notif.get('is_read') is is_read
        ]
    return jsonify(sorted_notifications), 200


@app_views.route('/users/<user_id>/notifications/<notification_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_notification(user_id, notification_id):
    """ deletes an notification belonging to particular user id given from storage """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    notification = storage.get(Notification, notification_id)
    if not notification:
        abort(404)
    notification.delete()
    storage.save()
    return jsonify({"success": True}), 201


@app_views.route('/users/<user_id>/notifications/<notification_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_notification(user_id, notification_id):
    """ updates the details of an notification """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    notification = storage.get(Notification, notification_id)
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
