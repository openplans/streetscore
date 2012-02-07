var StreetScore = StreetScore || {};

(function(S) {
  S.SurveyView = Backbone.View.extend({
    className: 'item',

    initialize: function() {
    },

    render: function() {
      var template = Mustache.template('survey');
      $(this.el).html(template.render(this.model.toJSON()));

      return this;
    },

    events : {
      'click .vote' : 'vote'
    },

    vote: function(e) {
      var newScore = $(e.currentTarget).attr('data-score');
      console.log(this.model.toJSON());
      console.log(newScore);
    }
  });

  S.AppView = Backbone.View.extend({
    el: '#survey-container',

    initialize: function() {
      this.model = new S.SurveySessionCollection();
      this.model.bind('reset', this.render, this);

      this.model.fetch();
    },

    render: function() {
      var self = this;

      this.model.each(function(surveyModel) {
        var view = new S.SurveyView( {model: surveyModel} );
        $(self.el).append(view.render().el);
      });

      if ($('.item', self.el).hasClass('active') === false) {
        $('.item:first', self.el).addClass('active');
      }

      $('.carousel').carousel();
      $('.carousel').carousel('pause');
    }
  });
})(StreetScore);

StreetScore.app = new StreetScore.AppView();
