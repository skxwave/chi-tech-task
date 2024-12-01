from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import select

from core import db
from core.models import Article
from ..helpers import get_user

bp = Blueprint("articles", __name__)


@bp.route("", methods=["GET"])
@jwt_required()
def get_all_articles():
    articles = db.session.scalars(select(Article)).all()
    return {"msg": [article.to_dict() for article in articles]}, 200


@bp.route("/<int:article_id>", methods=["GET"])
@jwt_required()
def get_article_by_id(article_id):
    article = db.session.scalar(select(Article).where(Article.id == article_id))

    if not article:
        return {"msg": "article not found"}, 404

    return {"msg": article.to_dict()}, 200


@bp.route("", methods=["POST"])
@jwt_required()
def create_article():
    user = get_user()
    data = request.get_json()

    if "title" not in data or "content" not in data:
        return {"msg": "fields missing"}, 400

    article = Article(
        title=data["title"],
        content=data["content"],
        user_id=user.id,
    )

    db.session.add(article)
    db.session.commit()

    return {"msg": article.to_dict()}, 201


@bp.route("/<int:article_id>", methods=["PUT"])
@jwt_required()
def update_article(article_id):
    user = get_user()
    article = db.session.scalar(select(Article).where(Article.id == article_id))
    data = request.get_json()

    if not article:
        return {"msg": "article not found"}, 404

    if user.role == "user" and user.id != article_id:
        return {"msg": "access denied"}, 403

    if not data:
        return {"msg": "fields missing"}, 400
    if "title" in data:
        article.title = data["title"]
    if "content" in data:
        article.content = data["content"]
    
    db.session.commit()

    return {"msg": "article updated", "result": article.to_dict()}, 200


@bp.route("/<int:article_id>", methods=["DELETE"])
@jwt_required()
def delete_article(article_id):
    user = get_user()
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
