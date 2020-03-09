from application import app, db, login_required
from application.animals.models import Animal
from application.auth.models import User
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user
from application.votes.models import Vote
import json


@app.route("/animals/list_suggested/vote/save", methods=["POST"])
@login_required()
def vote():
    try:
        accepted_suggestions = 0
        deleted_suggestions = 0
        to_delete = json.loads(str(request.json["to_delete"]))
        downvotes = json.loads(str(request.json["downvotes"]))
        upvotes = json.loads(str(request.json["upvotes"]))

        amount_of_suggestions = Animal.query.filter(Animal.suggestion_flag == True).count()
        # Check that the request only contains changes for 0 to 500 votes.
        if ((len(to_delete) + len(downvotes) + len(upvotes) > 0) and (len(to_delete) + len(downvotes) + len(upvotes) <= amount_of_suggestions)):
            # Check for resending of same request and for nonexisting suggestion ids.
            downvote_ids = db.session.query(Vote.animal_id).filter(Vote.account_id == current_user.account_id, Vote.value == False).all()
            upvote_ids = db.session.query(Vote.animal_id).filter(Vote.account_id == current_user.account_id, Vote.value == True).all()
            if len(upvote_ids) > 0:
                upvote_ids = set(unpack_votes_to_array(upvote_ids))
            if len(downvote_ids) > 0:
                downvote_ids = set(unpack_votes_to_array(downvote_ids))
            downvotes_set = set(downvotes)
            upvotes_set = set(upvotes)
            d_res = downvotes_set.difference(downvote_ids)
            u_res = upvotes_set.difference(upvote_ids)
            if len(d_res) != len(downvotes) or len(u_res) != len(upvotes):
                return jsonify({"Result": "DataError, nice try."})

            acc_id = current_user.account_id
            # Handle votes that are deleted, meaning that the user retracts their vote
            deleted, accepted = handle_to_delete(to_delete, acc_id)
            accepted_suggestions = accepted + accepted_suggestions
            deleted_suggestions = deleted + deleted_suggestions
            # Handle downvotes
            deleted_suggestions = deleted_suggestions + handle_downvotes(downvotes, acc_id)
            # Handle upvotes
            accepted_suggestions = accepted_suggestions + handle_upvotes(upvotes, acc_id)
            db.session.commit()
            if accepted_suggestions > 0 or deleted_suggestions > 0:
                flash_deleted_or_accepted_amount(accepted_suggestions, deleted_suggestions)
                return jsonify({"Result": "Success!", "New_Animals_Added": accepted_suggestions, "Suggestions_deleted": deleted_suggestions})
            else:
                return jsonify({"Result": "Success!", "New_Animals_Added": accepted_suggestions, "Suggestions_deleted": deleted_suggestions}) 
        else:
            flash("Äänidata oli virheellistä!", "error")
            return jsonify({"Result": "DataError"})
    except Exception as e:
        db.session.rollback()
        flash("Äänien tallentamisessa tapahtui virhe!", "error")
        return jsonify({"Result": "Exception", "Exception_message": str(e)})



@app.route("/animals/list_suggested/vote/get_votes", methods=["GET"])
@login_required()
def voteCheck():
    user_votes = db.session.query(Vote.animal_id, Vote.value).filter_by(account_id=current_user.get_id()).all()
    return jsonify(serialize(user_votes))


def handle_to_delete(to_delete, current_user_id):
    deleted = 0
    accepted = 0
    for suggestion_id in to_delete:
        vote = Vote.query.filter(Vote.animal_id == suggestion_id, Vote.account_id == current_user_id).first()
        # Handle nonexistent votes
        if vote is None:
            break

        suggestion = Animal.query.get(suggestion_id)
        if vote.value:
            if suggestion.votes_num - 1 < -2:
                suggestion_owner = User.query.get(suggestion.account_id)
                if suggestion_owner is not None:
                    suggestion_owner.suggestions_deleted = suggestion_owner.suggestions_deleted + 1
                Vote.query.filter(Vote.animal_id == suggestion.animal_id).delete()
                db.session.delete(suggestion)
                deleted = deleted + 1
            else:
                suggestion.votes_num = suggestion.votes_num - 1
        else:
            if suggestion.votes_num + 1 > 2 and suggestion.suggestion_flag == True:
                suggestion_owner = User.query.get(suggestion.account_id)
                if suggestion_owner is not None:
                    suggestion_owner.suggestions_accepted = suggestion_owner.suggestions_accepted + 1
                suggestion.suggestion_flag = False
                accepted = accepted + 1
                Vote.query.filter(Vote.animal_id == suggestion.animal_id).delete()
            else:
                suggestion.votes_num = suggestion.votes_num + 1
        db.session.delete(vote)
    return deleted, accepted


def handle_downvotes(downvotes, current_user_id):
    deleted = 0
    for suggestion_id in downvotes:
        vote = Vote.query.filter(
            Vote.animal_id == suggestion_id, Vote.account_id == current_user_id).first()
        suggestion = Animal.query.get(suggestion_id)
        if vote is None:
            if suggestion.votes_num - 1 < -2:
                suggestion_owner = User.query.get(suggestion.account_id)
                if suggestion_owner is not None:
                    suggestion_owner.suggestions_deleted = suggestion_owner.suggestions_deleted + 1
                Vote.query.filter(Vote.animal_id == suggestion.animal_id).delete()
                db.session.delete(suggestion)
                deleted = deleted + 1
            else:
                vote = Vote(False, suggestion_id, current_user_id)
                db.session.add(vote)
                suggestion.votes_num = suggestion.votes_num - 1
        else:
            if suggestion.votes_num - 2 < -2:
                suggestion_owner = User.query.get(suggestion.account_id)
                if suggestion_owner is not None:
                    suggestion_owner.suggestions_deleted = suggestion_owner.suggestions_deleted + 1
                Vote.query.filter(Vote.animal_id == suggestion.animal_id).delete()
                db.session.delete(suggestion)
                deleted = deleted + 1
            else:
                vote.value = False
                suggestion.votes_num = suggestion.votes_num - 2
    return deleted


def handle_upvotes(upvotes, current_user_id):
    accepted = 0
    for suggestion_id in upvotes:
        vote = Vote.query.filter(
            Vote.animal_id == suggestion_id, Vote.account_id == current_user_id).first()
        suggestion = Animal.query.get(suggestion_id)
        if vote is None:
            if suggestion.votes_num + 1 > 2 and suggestion.suggestion_flag == True:
                suggestion_owner = User.query.get(suggestion.account_id)
                if suggestion_owner is not None:
                    suggestion_owner.suggestions_accepted = suggestion_owner.suggestions_accepted + 1
                suggestion.suggestion_flag = False
                accepted = accepted + 1
                Vote.query.filter(Vote.animal_id == suggestion.animal_id).delete()
            else:
                vote = Vote(True, suggestion_id, current_user_id)
                db.session.add(vote)
                suggestion.votes_num = suggestion.votes_num + 1
        else:
            if suggestion.votes_num + 2 > 2 and suggestion.suggestion_flag == True:
                suggestion_owner = User.query.get(suggestion.account_id)
                if suggestion is not None:
                    suggestion_owner.suggestions_accepted = suggestion_owner.suggestions_accepted + 1
                suggestion.suggestion_flag = False
                accepted = accepted + 1
                Vote.query.filter(Vote.animal_id == suggestion.animal_id).delete()
            else:
                vote.value = True
                suggestion.votes_num = suggestion.votes_num + 2
    return accepted

def flash_deleted_or_accepted_amount(acc, dele):
    acc_string = ""
    dele_string = ""
    if acc == 1:
        acc_string = "{} ehdotus hyväksyttiin!".format(acc)
    elif acc > 1:
        acc_string = "{} ehdotusta hyväksyttiin!".format(acc)
    if dele == 1:
        dele_string = "{} ehdotus poistettiin".format(dele)
    elif dele > 1:
        dele_string = "{} ehdotusta poistettiin".format(dele)
    if len(dele_string) > 0 and len(acc_string) > 0:
        acc_string = acc_string + "\n"
    return flash(acc_string + dele_string, "info")

def serialize(votes):
    array = []
    for vote in votes:
        array.append({"vote": {
            "suggestion_id": vote.animal_id,
            "value": vote.value}})
    return array

def unpack_votes_to_array(votes):
    array = []
    for vote in votes:
        array.append(vote[0])
    return array