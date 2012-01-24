var StreetScore = StreetScore || {};

(function(S) {
  S.StreetView = Backbone.View.extend({
    initialize: function() {
      // Init Google Street View
      this.sv = new google.maps.StreetViewService();
      this.pano =  new google.maps.StreetViewPanorama(document.getElementById('streetview-container'));

      // Bind model change event
      this.model.bind('change', this.render, this);
    },

    render: function() {
      var latLng = new google.maps.LatLng(this.model.get('point').lat, this.model.get('point').lon);
      var view = this;

      this.sv.getPanoramaByLocation(latLng, 50, function(data, status){
        view.pano.setPano(data.location.pano);
        view.pano.setPov({
          heading: 270,
          pitch: 0,
          zoom: 1
        });
        view.pano.setVisible(true);
      });
    }
  });

  /**
   * The view class for a list of ratings.
   */
  S.RatingsView = Backbone.View.extend({
    initialize: function() {
      this.$container = $('ul#rating-list');

      // Bind model change event
      this.model.bind('change', this.render, this);
    },

    render: function() {
      var questions = this.model.get('questions')
        , ratings = new S.RatingCollection()
        , listView = this;

      // Empty the list before appending
      listView.$container.empty();

      // As we add new ratings to the collection, we want new views to be
      // associated with them.
      ratings.bind('add', function(rating) {
        var itemView = new S.RatingView({model: rating});
        listView.$container.append(itemView.render().el);
      });

      // Loop through the questions, creating a corresponding RatingModel for
      // each.  We add them to the collection instead of just creating them
      // directly because the collection is how they know their URL.
      _.each(questions, function(question){
        ratings.add({
          'criterion': question.id,
          'question': question.prompt,
          'score': 0,
          'segment': listView.model.get('segment_id'),
          'block_index': listView.model.get('block_index')
        });
      });

      return this;
    }
  });

  /**
   * The view class for a single rating model.  Constructed as a sub-view of
   * a RatingsView.
   */
  S.RatingView = Backbone.View.extend({
    tagName: 'li',

    initialize: function() {
      this.model.bind('change', this.render, this);
    },

    events: {
      'change [name="score"]' : 'setScore'
    },

    render: function() {
      var template = Mustache.template('rating')
        , rating = this.model
        , html = template.render(rating.toJSON());

      $(this.el).html(html);
      return this;
    },

    setScore: function() {
      var newScore = this.$('[name="score"]').val();
      this.model.set({'score': newScore});

      // HACK: I'm not sure the right way to do this.  I want to not send these
      //       two attributes to the server.
      this.model.unset('id');
      this.model.unset('url');

      this.model.save();
    }
  });

  S.AppView = Backbone.View.extend({
    initialize: function() {
      var model = new S.SurveySessionModel(),
          streetView = new StreetScore.StreetView({ model: model }),
          ratingsView = new StreetScore.RatingsView({ model: model });

      model.fetch();

      // Fetch a new street segment and questions
      $('a#next-survey').click(function(){
        model.fetch();
      });
    }
  });
})(StreetScore);

var app = new StreetScore.AppView();
