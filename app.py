from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "its_my_secret"

connect_db(app)




@app.route("/api/cupcakes")
def list_cupcakes():
    """Return JSON with all Cupcakes"""
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Returns JSON for one specifice cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Creates a new cupcake and returns JSON of the created item"""
    new_cupcake = Cupcake(flavor=request.json["flavor"],
                          rating=request.json["rating"],
                          size=request.json["size"],
                          image=request.json["image"] or None)
    
    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()), 201)



@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Updates a cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get['flavor', cupcake.flavor]
    cupcake.rating = request.json.get['rating', cupcake.rating]
    cupcake.size = request.json.get['size', cupcake.size]
    cupcake.image = request.json.get['image', cupcake.image]

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    """Delete cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="deleted")

@app.route("/")
def root():
    """Display homepage with list of cupcakes"""
    # cupcakes = Cupcake.query.all()
    return render_template("index.html")
