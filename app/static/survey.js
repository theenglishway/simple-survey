Survey
    .StylesManager
    .applyTheme("default");

function setupSurvey(survey_name) {
    document.addEventListener("DOMContentLoaded", function(event) {
        var xhr_get = new XMLHttpRequest();
        xhr_get.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var json = JSON.parse(this.responseText);
                window.survey = new Survey.Model(json);

                survey
                    .onComplete
                    .add(function (result, options) {
                      var xhr_post = new XMLHttpRequest();
                      xhr_post.open("POST", `/polls/${survey_name}/results`);
                      xhr_post.setRequestHeader("Content-Type", "application/json; charset=utf-8");
                      xhr_post.send(JSON.stringify(result.data));
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
        xhr_get.open("GET", `/surveys/${survey_name}`, true);
        xhr_get.setRequestHeader("Content-Type", "application/json; charset=utf-8");
        xhr_get.send();
    });
}
