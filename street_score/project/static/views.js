var StreetScore = StreetScore || {};

(function(S) {
  S.sv = new google.maps.StreetViewService();


  S.StreetImageView = Backbone.View.extend({
    tagName: 'img',

    initialize: function() {
    },

    render: function(success, error) {
      var self = this,
          latLng = new google.maps.LatLng(self.options.point.lat, self.options.point.lon);

      S.sv.getPanoramaByLocation(latLng, 50, function(data, status) {
        if (status === google.maps.StreetViewStatus.OK) {
          var url = 'http://maps.googleapis.com/maps/api/streetview?size=600x600&location='+
            self.options.point.lat+','+self.options.point.lon+'&heading=0&fov=90&pitch=5&sensor=false';

          $(self.el).attr('src', url);

          if (success) { success(self.el); }
        } else {
          if (error) { error(); }
        }
      });
    }
  });

  S.SurveyView = Backbone.View.extend({
    className: 'item',

    initialize: function() {
      console.log(this.model.toJSON());
    },

    render: function(success, error) {
      var self = this,
          sv1 = new S.StreetImageView({point: this.options.point1}),
          sv2 = new S.StreetImageView({point: this.options.point2});

      // Attempt to render street view 1, success or
      sv1.render(function(el1){
        sv2.render(function(el2){
          // Both points have street view, so render...
          var template = Mustache.template('survey');
          $(self.el).html(template.render(self.model.toJSON()));

          // Append street views
          $('.first.survey-choice', self.el).append(el1);
          $('.second.survey-choice', self.el).append(el2);

          if (success) {success(self.el);}
        }, function(){
          if (error) {error();}
        });
      }, function(){
        if (error) {error();}
      });
    },

    events : {
      'click .vote' : 'vote'
    },

    vote: function(e) {
      var newScore = $(e.currentTarget).attr('data-score');
      console.log(newScore);

      this.model.save({'score': newScore});
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
        var question = surveyModel.get('questions')[0],
            blocks = surveyModel.get('blocks'),
            ratingModel = new S.RatingModel({
              'criterion': question.id,
              'question': question.prompt,
              'score': 0,
              'segment1': blocks[0].segment_id,
              'block1_index': blocks[0].block_index,
              'segment2': blocks[1].segment_id,
              'block2_index': blocks[1].block_index
            }),
            view = new S.SurveyView( {
              model: ratingModel,
              point1: surveyModel.get('blocks')[0].point,
              point2: surveyModel.get('blocks')[1].point
            });

        view.render(function(el) {
          $(self.el).append(el);

          if ($('.item', self.el).hasClass('active') === false) {
            $('.item:first', self.el).addClass('active');
          }

          $('.carousel').carousel({interval: 36000000});
        });
      });
    }
  });
})(StreetScore);

StreetScore.app = new StreetScore.AppView();
