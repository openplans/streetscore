var StreetScore = StreetScore || {};

(function(S) {
  S.SurveySessionModel = Backbone.Model.extend({});
  S.SurveySessionCollection = Backbone.Collection.extend({
    url: '/survey_sessions/',
    model: S.SurveySessionModel
  });

  S.RatingModel = Backbone.Model.extend({
    urlRoot: '/ratings/'
  });

  S.UserInfoModel = Backbone.Model.extend({
    urlRoot: '/user_info/'
  });
})(StreetScore);
