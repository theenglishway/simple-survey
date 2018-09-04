Survey
    .StylesManager
    .applyTheme("default");

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var json = JSON.parse(this.responseText);
        window.survey = new Survey.Model(json);

        survey
            .onComplete
            .add(function (result, options) {
              var xhr = new XMLHttpRequest();
              xhr.open("POST", "/results");
              xhr.setRequestHeader("Content-Type", "application/json; charset=utf-8");
              xhr.send(JSON.stringify(result.data));
              document
                  .querySelector('#surveyResult')
                  .innerHTML = "result: " + JSON.stringify(result.data);
            });

        var app = new Vue({
            el: '#surveyElement',
            data: {
                survey: survey
            }
        });
    }
};
xhttp.open("GET", "/static/survey.json", true);
xhttp.send();
