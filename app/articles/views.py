from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select

from core import db
from core.models import User, Article

bp = Blueprint("articles", __name__)


@bp.route("", methods=["GET"])
@jwt_required()
def get_all_articles():
    articles = db.session.scalars(select(Article)).all()
    return {"msg": [article.to_dict() for article in articles]}, 200


@bp.route("", methods=["POST"])
@jwt_required()
def create_article():
    username = get_jwt_identity()
    user = db.session.scalar(select(User).where(User.username == username))
    data = request.get_json()
    if not data["title"] or not data["content"]:
        return {"error": "Title and content are required"}, 400

    article = Article(
        title=data["title"],
        content=data["content"],
        user_id=user.id,
    )

    db.session.add(article)
    db.session.commit()

    return {"msg": article.to_dict()}


@bp.route("/<int:article_id>", methods=["PUT"])
@jwt_required()
def update_article(article_id):
    username = get_jwt_identity()
    user = db.session.scalar(select(User).where(User.username == username))
    article = db.session.scalar(select(Article).where(Article.id == article_id))

    if not article:
        return {"msg": "article not found"}, 404

    if user.role == "user" and user.id != article_id:
        return {"msg": "access denied"}, 403

    data = request.get_json()
    article.title = data["title"]
    article.content = data["content"]
    db.session.commit()

    return {"msg": "article updated", "result": article.to_dict()}, 200


@bp.route("/<int:article_id>", methods=["DELETE"])
@jwt_required()
def delete_article(article_id):
    username = get_jwt_identity()
    user = db.session.scalar(select(User).where(User.username == username))
    article = db.session.scalar(select(Article).where(Article.id == article_id))

    if not article:
        return {"msg": "article not found"}, 404

    if user.role in ["user", "editor"] and user.id != article_id:
        return {"msg": "access denied"}, 403

    db.session.delete(article)
    db.session.commit()
    return {"msg": "deleted successfully"}, 200


@bp.route("/search", methods=["GET"])
@jwt_required()
def search_article():
    query = request.args.get("q", "")
    articles = db.session.scalars(
        select(Article).filter(
            Article.title.ilike(f"%{query}%") | Article.content.ilike(f"%{query}%")
        )
    ).all()
    return {"msg": [article.to_dict() for article in articles]}
