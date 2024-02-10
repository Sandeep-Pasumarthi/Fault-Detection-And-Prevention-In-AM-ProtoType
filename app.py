from flask import Flask, request, render_template
from prediction_service.prediction import make_prediction
import os


webapp_root = "web_app"
cols_to_change = ["TWF", "HDF", "PWF", "OSF", "RNF"]

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)


def change_data_dict(data_dict):
    try:
        new_data = dict()
        for i in data_dict.keys():
            if i in cols_to_change:
                if data_dict[i] == str(0):
                    new_data[i] = "No"
                else:
                    new_data[i] = "Yes"
            else:
                new_data[i] = data_dict[i]
        return new_data
    except Exception as e:
        print(str(e))


@app.route("/", methods=["POST", "GET"])
def home():
    try:
        if request.method == "POST":
            data_dict = dict(request.form)
            final_data_dict = change_data_dict(data_dict)
            prediction, probability = make_prediction(data_dict)
            if prediction == 0:
                return render_template("result.html", data=final_data_dict, prediction="No Failure")
            else:
                return render_template("result.html", data=final_data_dict, prediction="Machine can Fail")
        else:
            return render_template("home.html")
    except Exception as e:
        print(str(e))
        return render_template("404.html", error="Entered some unusual values! Please check your values again.")


if __name__ == "__main__":
    app.run(debug=True)
