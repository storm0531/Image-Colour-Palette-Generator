from flask import Flask,render_template,redirect,url_for,request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField,IntegerField
from wtforms.validators import DataRequired,NumberRange
from flask_bootstrap import Bootstrap
import colorgram

all_colors = []

class UploadForm(FlaskForm):
    image = FileField("image input",validators=[FileRequired(),
                                                FileAllowed(['jpg', 'png'], 'Images only!')])
    color_count = IntegerField(
        description="choose number of colors to extract",
        validators=[DataRequired(),NumberRange(min=1,max=60)],
                         )
    submit = SubmitField("extract")

app= Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = "SECRET_KEY"

@app.route("/",methods=["GET","POST"])
def get_image():
    global all_colors
    form = UploadForm()
    if form.validate_on_submit():
        img = form.image.data
        color_num = form.color_count.data

        all_colors = []
        colors = colorgram.extract(img,color_num)
        for color in colors:
            red = color.rgb.r
            blue = color.rgb.b
            green = color.rgb.g
            rgb_color = (red,blue,green)
            all_colors.append(rgb_color)

        return redirect(url_for("results"))
    return render_template("index.html",form=form)

@app.route("/results")
def results():
    return render_template("results.html",colors=all_colors)

if __name__ == "__main__":
    app.run(debug=True)