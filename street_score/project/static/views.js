var StreetScore = StreetScore || {};

(function(S) {
  S.sv = new google.maps.StreetViewService();

  // View to render a full Street View panel
  S.StreetviewView = Backbone.View.extend({
    className: 'streetview',

    initialize: function() {
      var self = this,
          heading = 0;

      // Init the panoramo object
      self.pano =  new google.maps.StreetViewPanorama(this.el, {
        linksControl: false,
        addressControl: false,
        zoomControlOptions: {
          style: google.maps.ZoomControlStyle.SMALL
        }
      });
    },

    render: function(success, error) {
      var self = this,
          latLng = new google.maps.LatLng(self.options.place.lat, self.options.place.lon);

      // Check for street view imagery, 50m radius
      S.sv.getPanoramaByLocation(latLng, 50, function(data, status) {
        if (status === google.maps.StreetViewStatus.OK) {
          // Setup the panorama
          self.pano.setPano(data.location.pano);
          self.pano.setPov({
            heading: 0,
            pitch: 5,
            zoom: 1
          });
          self.pano.setVisible(false);

          if (success) {success(self.el);}
        } else {
          if (error) { error(); }
        }
      });
    },

    events : {
      'mousedown' : 'stopRotation'
    },

    show: function() {
      var self = this,
          heading = 0;

      // Make the panorama visible
      self.pano.setVisible(true);

      // http://stackoverflow.com/questions/6809573/google-street-view-problem-javascript
      google.maps.event.trigger(self.pano, 'resize');

      if (self.options.rotate) {
        self.rotate_id = setInterval(function(){
          self.pano.setPov({
            heading: heading+=0.5,
            pitch: 5,
            zoom: 1
          });
        }, 40);
      }
    },

    stopRotation: function() {
      // Stop rotating street view on mousedown
      if (this.rotate_id) {
        clearInterval(this.rotate_id);
      }
    }
  });

  // Static street view images
  S.StreetImageView = Backbone.View.extend({
    tagName: 'img',
    className: 'streetview',

    render: function(success, error) {
      var self = this,
          latLng = new google.maps.LatLng(self.options.place.lat, self.options.place.lon);

      // Check for street view imagery, 50m radius
      S.sv.getPanoramaByLocation(latLng, 50, function(data, status) {
        if (status === google.maps.StreetViewStatus.OK) {
          if (success) { success(self.el); }
        } else {
          if (error) { error(); }
        }
      });
    },

    show: function(){
      var self = this,
          url = 'http://maps.googleapis.com/maps/api/streetview?size=550x550&location='+
          self.options.place.lat+','+self.options.place.lon+'&heading=0&fov=90&pitch=5&sensor=false';

      $(self.el).attr('src', url);
    }
  });

  // View for an entire survey, including two SVs to compare
  S.SurveyView = Backbone.View.extend({
    // Bootstrap carousels want this class
    className: 'item',

    initialize: function() {
      var self = this;

      // When a survey is shown, so the SV views
      $(document).on('show', function(e) {
        if (self.sv1.stopRotation) {self.sv1.stopRotation();}
        if (self.sv2.stopRotation) {self.sv2.stopRotation();}

        if ($(self.el).is('.active')) {
          // Remove previous surveys from the DOM
          $(self.el).prevAll().remove();

          self.sv1.show();
          self.sv2.show();
        }
      });
    },

    render: function(success, error) {
      var self = this;
      self.sv1 = new S.StreetviewView({place: this.model.get('place1'), rotate: false});
      self.sv2 = new S.StreetviewView({place: this.model.get('place2'), rotate: false});

      // Attempt to render street view 1, success or
      self.sv1.render(function(el1){
        self.sv2.render(function(el2){
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
      // Record a score and go the next survey
      var newScore = $(e.currentTarget).attr('data-score');

      // We only need the id/foreign key when saving. No need to
      // trigger the change event in this case even though it's
      // not bound.
      this.model.set({
        'place1': this.model.get('place1').id,
        'place2': this.model.get('place2').id
      }, {'silent': true});

      this.model.save({'score': newScore});
      $(S).trigger('vote');
    }
  });

  // UI stuff associated with locating a user
  S.LocateView = Backbone.View.extend({
    // Didn't use .locate-btn-container b/c BackBone only gave us back the
    // first element, and we wanted all of them. Using body for event context.
    el: 'body',

    initialize: function() {
      var self = this;

      self.model.bind('change', self.render, self);

      self.render();
    },

    render: function() {
      var self = this,
          template = Mustache.template('locate'),
          title = 'Save my Location';

      // Set the button title depending on whether a location exists or not
      if (self.model.get('lat') && self.model.get('lon')) {
        title = 'Update my Location';
      }

      // Render the buttons (now on the subnav and modal)
      $('.locate-btn-container').html(template.render({'title': title}));
    },

    events : {
      'click .locate-btn-container' : 'locate'
    },

    locate: function(){
      var self = this,
          $btn = $(self.el).find('.locate-btn');

      // Set loading status using 'data-loading-text' attribute
      $btn.button('loading');

      // Get the location
      navigator.geolocation.getCurrentPosition(function(position){

        // Save the location to the model
        self.model.save({
          'lat': position.coords.latitude,
          'lon': position.coords.longitude,
          'location_source': 'html5',
          'location_data': position
        });

        // Reset the buttons status
        $btn.button('reset');

        // Show the success message
        self.showMessage('Location saved. Thanks!', 'success');
      }, function(err){
        $btn.button('reset');
        // Didn't work. Show a helpful error.
        self.showMessage('Eeek. That didn\'t work. Please check your browser settings.', 'error');
      });
    },

    // Helper to show a status message
    showMessage: function(msg, status){

      $('<div class="locate-alert alert alert-'+(status || 'info')+'">' + msg + '</div>')
        .appendTo(this.el) // Append to the body
        .slideDown(300, function() {
          var self = this;
          setTimeout(function() { $(self).slideUp(); }, 3000);
        });
    }
  });

  // UI stuff for showing vote counts
  S.VoteCounter = Backbone.View.extend({
    el: '.vote-count',

    voteCount: 0,

    initialize: function(){
      var self = this;

      // Increment and update on vote. This is calculated so there's no need
      // to save it to the database.
      $(S).bind('vote', function(){
        self.options.voteCount++;
        self.render();
      });

      self.render();
    },

    render: function(){
      $(this.el).html(this.options.voteCount);
    }
  });

  // The view for the app, of course
  S.AppView = Backbone.View.extend({
    el: '#survey-container',

    initialize: function() {
      var self = this,
          QUEUE_SIZE = 4;

      self.model = new S.SurveySessionCollection();

      // Render thyself when the surveys show up
      self.model.bind('reset', self.render, self);

      // Tells the carousel to advance ot the next survey
      // and fetch more surveys from the server.
      $(S).on('next', function(){
        $('.carousel').carousel('next');

        // Only fetch surveys the total number of surveys we need
        var surveysToFetch = QUEUE_SIZE - $('.item:not(.active)').length;
        // console.log('fetching ' + surveysToFetch + ' surveys.');
        if (surveysToFetch > 0) {
          self.model.fetch({ data: {count:surveysToFetch} });
        }
      });

      // Trigger a more generic 'show' event when the carousel
      // advances to the next survey. The surveys sometimes need
      // to do something.
      $(document).on('slid', '.carousel', function(){
        $(document).triggerHandler('show');
      });

      // Listen for a vote event
      $(S).bind('vote', function(){
        $(S).trigger('next');
      });

      // Skip the current survey on link click
      $(document).on('click', '#skip', function() {
        $(S).trigger('next');
      });

      // Fetch the first batch of surveys
      self.model.fetch({ data: {count:QUEUE_SIZE} });

      // Init the carousel widget with a very large autoslide interval.
      $('.carousel').carousel({interval: 3600000});


      var voteCounterView = new S.VoteCounter({
        voteCount: self.options.initialVoteCount
      });

      var locateView = new S.LocateView({
        'model': new S.UserInfoModel({
          'id': self.options.userInfoId,
          'lat': self.options.userInfoLat,
          'lon': self.options.userInfoLon,
          'session': self.options.userInfoSessionKey
        })
      });
    },

    render: function() {
      var self = this;

      // Turn each survey model into a rating model so we can
      // rate each street view.
      this.model.each(function(surveyModel) {
        var question = surveyModel.get('questions')[0],
            places = surveyModel.get('places'),
            ratingModel = new S.RatingModel({
              'criterion': question.id,
              'question': question.prompt,
              'score': 0,
              'place1': places[0],
              'place2': places[1],
              'user_info': self.options.userInfoId
            }),
            // Make the survey, not yet rendered
            surveyView = new S.SurveyView( {
              model: ratingModel
            });

        // Render the survey view...
        surveyView.render(function(el) {
          // ...then append it to the DOM if streetview exists for both places
          $(self.el).append(el);

          // Make sure an item is active to make the carousel happy
          if ($('.item', self.el).hasClass('active') === false) {
            $('.item:first', self.el).addClass('active');
            // First time, make sure show is triggered
            setTimeout(function(){$(document).triggerHandler('show');},200);
          }
        });
      });
    }
  });
})(StreetScore);
