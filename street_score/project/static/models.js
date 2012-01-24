var StreetScore = StreetScore || {};

(function(S) {
  S.SurveySessionModel = Backbone.Model.extend({
    url: function() {
      return '/survey_session';
    }
  });

  S.RatingModel = Backbone.Model.extend({});
  S.RatingCollection = Backbone.Collection.extend({
    url: '/ratings/',
    model: S.RatingModel
  });

})(StreetScore);
