var StreetScore = StreetScore || {};

(function(S) {
  S.SurveySessionModel = Backbone.Model.extend({
    url: function() {
      return '/survey_session';
    }
  });


})(StreetScore);