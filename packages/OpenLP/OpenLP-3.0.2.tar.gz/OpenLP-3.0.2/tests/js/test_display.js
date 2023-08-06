function _createDiv(attrs) {
    var div = document.createElement("div");
    for (key in attrs) {
        div.setAttribute(key, attrs[key]);
    }
    document.body.appendChild(div);
    return div;
}

describe("The enumeration object", function () {
  it("BackgroundType should exist", function () {
    expect(BackgroundType).toBeDefined();
  });

  it("GradientType should exist", function () {
    expect(GradientType).toBeDefined();
  });

  it("HorizontalAlign should exist", function () {
    expect(HorizontalAlign).toBeDefined();
  });

  it("VerticalAlign should exist", function () {
    expect(VerticalAlign).toBeDefined();
  });

  it("AudioState should exist", function () {
    expect(AudioState).toBeDefined();
  });

  it("TransitionState should exist", function(){
    expect(TransitionState).toBeDefined();
  });

  it("AnimationState should exist", function(){
    expect(AnimationState).toBeDefined();
  });
});

describe("The function", function () {
  it("$() should return the right element", function () {
    var div = _createDiv({"id": "dollar-test"});
    expect($("#dollar-test")[0]).toBe(div);
  });

  it("_buildLinearGradient() should build the correct string", function () {
    var gradient = _buildLinearGradient("to bottom", "#000", "#fff");
    expect(gradient).toBe("linear-gradient(to bottom, #000, #fff) fixed");
  });

  it("_buildRadialGradient() should build the correct string", function () {
    var gradient = _buildRadialGradient(10, "#000", "#fff");
    expect(gradient).toBe("radial-gradient(#000, #fff) fixed");
  });

  it("_buildTextOutline should return an array of text-shadow values", function () {
    let shadows = _buildTextOutline(2, "#fff");
    expect(shadows).toEqual([
      "#fff -2pt -2pt 0pt",
      "#fff -2pt -1pt 0pt",
      "#fff -2pt 0pt 0pt",
      "#fff -2pt 1pt 0pt",
      "#fff -2pt 2pt 0pt",
      "#fff -1pt -2pt 0pt",
      "#fff -1pt -1pt 0pt",
      "#fff -1pt 0pt 0pt",
      "#fff -1pt 1pt 0pt",
      "#fff -1pt 2pt 0pt",
      "#fff 0pt -2pt 0pt",
      "#fff 0pt -1pt 0pt",
      "#fff 0pt 0pt 0pt",
      "#fff 0pt 1pt 0pt",
      "#fff 0pt 2pt 0pt",
      "#fff 1pt -2pt 0pt",
      "#fff 1pt -1pt 0pt",
      "#fff 1pt 0pt 0pt",
      "#fff 1pt 1pt 0pt",
      "#fff 1pt 2pt 0pt",
      "#fff 2pt -2pt 0pt",
      "#fff 2pt -1pt 0pt",
      "#fff 2pt 0pt 0pt",
      "#fff 2pt 1pt 0pt",
      "#fff 2pt 2pt 0pt"
    ]);
  });

  it("_buildTextShadow should return a string of text-shadow", function () {
    let shadow = _buildTextShadow(2, 2, "#acf");
    expect(shadow).toEqual([
      "#acf 0pt 0pt 0pt",
      "#acf 0pt 1pt 0pt",
      "#acf 0pt 2pt 0pt",
      "#acf 0pt 3pt 0pt",
      "#acf 0pt 4pt 0pt",
      "#acf 1pt 0pt 0pt",
      "#acf 1pt 1pt 0pt",
      "#acf 1pt 2pt 0pt",
      "#acf 1pt 3pt 0pt",
      "#acf 1pt 4pt 0pt",
      "#acf 2pt 0pt 0pt",
      "#acf 2pt 1pt 0pt",
      "#acf 2pt 2pt 0pt",
      "#acf 2pt 3pt 0pt",
      "#acf 2pt 4pt 0pt",
      "#acf 3pt 0pt 0pt",
      "#acf 3pt 1pt 0pt",
      "#acf 3pt 2pt 0pt",
      "#acf 3pt 3pt 0pt",
      "#acf 3pt 4pt 0pt",
      "#acf 4pt 0pt 0pt",
      "#acf 4pt 1pt 0pt",
      "#acf 4pt 2pt 0pt",
      "#acf 4pt 3pt 0pt",
      "#acf 4pt 4pt 0pt"
    ].join(", "));
  });

  it("_getStyle should return the correct style on an element", function () {
    var div = _createDiv({"id": "style-test"});
    div.style.setProperty("width", "100px");
    expect(_getStyle($("#style-test")[0], "width")).toBe("100px");
  });

  it("_nl2br should turn UNIX newlines into <br> tags", function () {
    var text = "Amazing grace, how sweet the sound\nThat saved a wretch like me";
    expect(_nl2br(text)).toEqual("Amazing grace, how sweet the sound<br>That saved a wretch like me");
  });

  it("_nl2br should turn Windows newlines into <br> tags", function () {
    var text = "Amazing grace, how sweet the sound\r\nThat saved a wretch like me";
    expect(_nl2br(text)).toEqual("Amazing grace, how sweet the sound<br>That saved a wretch like me");
  });

  it("_prepareText should turn verse text into a paragraph", function () {
    var text = "Amazing grace, how sweet the sound\nThat saved a wretch like me";
    expect(_prepareText(text)).toEqual("<p>Amazing grace, how sweet the sound<br>That saved a wretch like me</p>");
  });
});

describe("The Display object", function () {

  it("should start with a blank _slides object", function () {
    expect(Display._slides).toEqual({});
  });

  it("should have the correct Reveal config", function () {
    expect(Display._revealConfig).toEqual({
      margin: 0.0,
      minScale: 1.0,
      maxScale: 1.0,
      controls: false,
      progress: false,
      history: false,
      keyboard: false,
      overview: false,
      center: false,
      touch: false,
      help: false,
      transition: "none",
      backgroundTransition: "none",
      viewDistance: 9999,
      width: "100%",
      height: "100%"
    });
  });

  it("should have an init() method", function () {
    expect(Display.init).toBeDefined();
  });

  it("should initialise Reveal when init is called", function () {
    spyOn(Reveal, "initialize");
    document.body.innerHTML = "";
    Display.init();
    expect(Reveal.initialize).toHaveBeenCalled();
  });

  it("should have checkerboard class when init is called when not display", function () {
    spyOn(Reveal, "initialize");
    document.body.innerHTML = "";
    document.body.classList = "";
    Display.init({isDisplay: false});
    expect(document.body.classList.contains('checkerboard')).toEqual(true);
  });

  it("should not have checkerboard class when init is called when is a display", function () {
    spyOn(Reveal, "initialize");
    document.body.innerHTML = "";
    document.body.classList = "";
    Display.init({isDisplay: true});
    expect(document.body.classList.contains('checkerboard')).toEqual(false);
  });

  it("should have a reinit() method", function () {
    expect(Display.reinit).toBeDefined();
  });

  it("should sync Reveal and set to first slide when reinit is called", function () {
    spyOn(Reveal, "sync");
    spyOn(Reveal, "slide");
    Display.reinit();
    expect(Reveal.sync).toHaveBeenCalled();
    expect(Reveal.slide).toHaveBeenCalledWith(0);
  });

  it("should have a setItemTransition() method", function () {
    expect(Display.setItemTransition).toBeDefined();
  });

  it("should have a correctly functioning clearSlides() method", function () {
    expect(Display.clearSlides).toBeDefined();

    var slidesDiv = _createDiv({"class": "slides"});
    slidesDiv.innerHTML = "<section><p></p></section>";
    Display._slidesContainer = slidesDiv;
    var footerDiv = _createDiv({"class": "footer"});
    Display._footerContainer = footerDiv;

    Display.clearSlides();
    expect($(".slides")[0].innerHTML).toEqual("");
    expect(Display._slides).toEqual({});
  });

  it("should have a correct goToSlide() method", function () {
    spyOn(Reveal, "slide");
    spyOn(Display, "_slides");
    Display._slides["v1"] = 0;

    Display.goToSlide("v1");
    expect(Reveal.slide).toHaveBeenCalledWith(0, 0);
  });

  it("should have an alert() method", function () {
    expect(Display.alert).toBeDefined();
  });

});

describe("Transitions", function () {
  beforeEach(function() {
    document.body.innerHTML = "";
    _createDiv({"class": "slides"});
    _createDiv({"class": "footer"});
    Display._slides = {};
  });
  afterEach(function() {
    // Reset theme
    Display._theme = null;
  });

  it("should have a correctly functioning setItemTransition() method", function () {
    spyOn(Reveal, "configure");
    Display.setItemTransition(true);
    expect(Reveal.configure).toHaveBeenCalledWith({"backgroundTransition": "fade", "transitionSpeed": "default"});
  });

  it("should have enabled transitions when _doTransitions is true and applyTheme is run", function () {
    Display._doTransitions = true;
    var theme = {
      "display_slide_transition": true,
      "display_slide_transition_type": TransitionType.Slide,
      "display_slide_transition_speed": TransitionSpeed.Fast
    }
    Display.setTheme(theme);
    var slidesDiv = _createDiv({"class": "slides"});
    slidesDiv.innerHTML = "<section><section><p></p></section></section>";
    Display._slidesContainer = slidesDiv;

    Display.applyTheme(Display._slidesContainer.children[0])

    expect(Display._slidesContainer.children[0].children[0].getAttribute("data-transition")).toEqual("slide-horizontal");
    expect(Display._slidesContainer.children[0].children[0].getAttribute("data-transition-speed")).toEqual("fast");
  });

  it("should have not enabled transitions when init() with no transitions and setTheme is run", function () {
    Display._doTransitions = false;
    var theme = {
      "display_slide_transition": true,
      "display_slide_transition_type": TransitionType.Slide,
      "display_slide_transition_speed": TransitionSpeed.Fast,
    }
    Display.setTheme(theme);
    var slidesDiv = _createDiv({"class": "slides"});
    slidesDiv.innerHTML = "<section><section><p></p></section></section>";
    Display._slidesContainer = slidesDiv;

    Display.applyTheme(Display._slidesContainer.children[0])

    expect(Display._slidesContainer.children[0].children[0].getAttribute("data-transition")).toEqual("none");
  });

  it("should have enabled transitions in the correct direction", function () {
    Display._doTransitions = true;
    var theme = {
      "display_slide_transition": true,
      "display_slide_transition_type": TransitionType.Convex,
      "display_slide_transition_speed": TransitionSpeed.Slow,
      "display_slide_transition_direction": TransitionDirection.Vertical,
      "display_slide_transition_reverse": true,
    }
    Display.setTheme(theme);
    var slidesDiv = _createDiv({"class": "slides"});
    slidesDiv.innerHTML = "<section><section><p></p></section></section>";
    Display._slidesContainer = slidesDiv;

    Display.applyTheme(Display._slidesContainer.children[0])

    expect(Display._slidesContainer.children[0].children[0].getAttribute("data-transition")).toEqual("convex-vertical-reverse");
    expect(Display._slidesContainer.children[0].children[0].getAttribute("data-transition-speed")).toEqual("slow");
  });
});


describe("Screen Visibility", function () {
  var TRANSITION_TIMEOUT = 2000;

  beforeEach(function() {
    window.displayWatcher = jasmine.createSpyObj('DisplayWatcher', ['dispatchEvent', 'setInitialised', 'pleaseRepaint']);
    document.body.innerHTML = "";
    var revealDiv = _createDiv({"class": "reveal"});
    var slidesDiv = _createDiv({"class": "slides"});
    var footerDiv = _createDiv({"class": "footer"});
    slidesDiv.innerHTML = "<section><section><p></p></section></section>";
    revealDiv.append(slidesDiv);
    revealDiv.append(footerDiv);
    document.body.style.transition = "opacity 75ms ease-in-out";
    Display.init({isDisplay: true, doItemTransition: false});
  });
  afterEach(function() {
    // Reset theme
    Display._theme = null;
  });

  it("should trigger dispatchEvent when toTransparent(eventName) is called with an event parameter", function (done) {
    var testEventName = 'event_32';
    displayWatcher.dispatchEvent = function(eventName) {
      if (eventName == testEventName) {
        done();
      }
    };

    Display.toTransparent(testEventName);

    setTimeout(function() {
      fail('dispatchEvent not called');
      done();
    }, TRANSITION_TIMEOUT);
  });

  it("should trigger dispatchEvent when toBlack(eventName) is called with an event parameter", function (done) {
    var testEventName = 'event_33';
    displayWatcher.dispatchEvent = function(eventName) {
      if (eventName == testEventName) {
        done();
      }
    };

    Display.toBlack(testEventName);

    setTimeout(function() {
      fail('dispatchEvent not called');
      done();
    }, TRANSITION_TIMEOUT);
  });

  it("should trigger dispatchEvent when toTheme(eventName) is called with an event parameter", function (done) {
    var testEventName = 'event_34';
    displayWatcher.dispatchEvent = function(eventName) {
      if (eventName == testEventName) {
        done();
      }
    };

    Display.toTheme(testEventName);

    setTimeout(function() {
      fail('dispatchEvent not called');
      done();
    }, TRANSITION_TIMEOUT);
  });

  it("should trigger dispatchEvent when show(eventName) is called with an event parameter", function (done) {
    var testEventName = 'event_35';
    displayWatcher.dispatchEvent = function(eventName) {
      if (eventName == testEventName) {
        done();
      }
    };

    Display.show(testEventName);

    setTimeout(function() {
      fail('dispatchEvent not called');
      done();
    }, TRANSITION_TIMEOUT);
  });
});

describe("Display.alert", function () {
  var alertContainer, alertBackground, alertText, settings, text;

  beforeEach(function () {
    document.body.innerHTML = "";
    alertContainer = _createDiv({"class": "alert-container"});
    alertBackground = _createDiv({"id": "alert-background", "class": "hide"});
    alertText = _createDiv({"id": "alert-text", "class": "hide"});
    settings = {
      "location": 1,
      "fontFace": "sans-serif",
      "fontSize": 40,
      "fontColor": "#ffffff",
      "backgroundColor": "#660000",
      "timeout": 5,
      "repeat": 1,
      "scroll": true
    };
    text = "Display.alert";
  });

  it("should return null if called without any text", function () {
    expect(Display.alert("", settings)).toBeNull();
  });

  it("should set the correct alert text", function () {
    spyOn(Display, "showAlert");

    Display.alert(text, settings);

    expect(Display.showAlert).toHaveBeenCalled();
  });

  it("should call the addAlertToQueue method if an alert is displaying", function () {
    spyOn(Display, "addAlertToQueue");
    Display._alerts = [];
    Display._alertState = AlertState.Displaying;

    Display.alert(text, settings);

    expect(Display.addAlertToQueue).toHaveBeenCalledWith(text, settings);
  });
});

describe("Display.showAlert", function () {
  var alertContainer, alertBackground, alertText, settings;

  beforeEach(function () {
    document.body.innerHTML = "";
    alertContainer = _createDiv({"class": "alert-container"});
    alertBackground = _createDiv({"id": "alert-background", "class": "hide"});
    alertText = _createDiv({"id": "alert-text", "class": "hide"});
    settings = {
      "location": 1,
      "fontFace": "sans-serif",
      "fontSize": 40,
      "fontColor": "#ffffff",
      "backgroundColor": "#660000",
      "timeout": 5,
      "repeat": 1,
      "scroll": true
    };
  });

  it("should create a stylesheet for the settings", function () {
    spyOn(window, "_createStyle");
    Display.showAlert("Test Display.showAlert - stylesheet", settings);

    expect(_createStyle).toHaveBeenCalledWith("#alert-background.settings", {
      backgroundColor: settings["backgroundColor"],
      fontFamily: "'" + settings["fontFace"] + "'",
      fontSize: settings["fontSize"] + 'pt',
      color: settings["fontColor"]
    });
  });

  it("should change fontFace to 'sans-serif' if no font face is provided", function () {
    spyOn(window, "_createStyle");
    Display.showAlert("Test Display.showAlert - fontFace fix", {
      "location": 1,
      "fontFace": "",
      "fontSize": 40,
      "fontColor": "#ffffff",
      "backgroundColor": "#660000",
      "timeout": 5,
      "repeat": 1,
      "scroll": true
    });

    expect(_createStyle).toHaveBeenCalledWith("#alert-background.settings", {
      backgroundColor: settings["backgroundColor"],
      fontFamily: "sans-serif",
      fontSize: settings["fontSize"] + 'pt',
      color: settings["fontColor"]
    });
  });

  it("should change fontFace to 'sans-serif' if 'Sans Serif' is provided", function () {
    spyOn(window, "_createStyle");
    Display.showAlert("Test Display.showAlert - fontFace fix", {
      "location": 1,
      "fontFace": "Sans Serif",
      "fontSize": 40,
      "fontColor": "#ffffff",
      "backgroundColor": "#660000",
      "timeout": 5,
      "repeat": 1,
      "scroll": true
    });

    expect(_createStyle).toHaveBeenCalledWith("#alert-background.settings", {
      backgroundColor: settings["backgroundColor"],
      fontFamily: "sans-serif",
      fontSize: settings["fontSize"] + 'pt',
      color: settings["fontColor"]
    });
  });

  it("should set the alert state to AlertState.Displaying", function () {
    Display.showAlert("Test Display.showAlert - state", settings);

    expect(Display._alertState).toEqual(AlertState.Displaying);
  });

  it("should remove the 'hide' classes and add the 'show' classes", function () {
    Display.showAlert("Test Display.showAlert - classes", settings);

    expect($("#alert-background")[0].classList.contains("hide")).toEqual(false);
    expect($("#alert-background")[0].classList.contains("show")).toEqual(true);
    expect($("#alert-text")[0].classList.contains("hide")).toEqual(false);
    expect($("#alert-text")[0].classList.contains("show")).toEqual(true);
  });
});

describe("Display.hideAlert", function () {
  var alertContainer, alertBackground, alertText, settings;

  beforeEach(function () {
    document.body.innerHTML = "";
    alertContainer = _createDiv({"class": "alert-container"});
    alertBackground = _createDiv({"id": "alert-background", "class": "hide"});
    alertText = _createDiv({"id": "alert-text", "class": "hide"});
    settings = {
      "location": 1,
      "fontFace": "sans-serif",
      "fontSize": 40,
      "fontColor": "#ffffff",
      "backgroundColor": "#660000",
      "timeout": 5,
      "repeat": 1,
      "scroll": true
    };
  });

  it("should set the alert state to AlertState.NotDisplaying", function () {
    Display.showAlert("test", settings);

    Display.hideAlert();

    expect(Display._alertState).toEqual(AlertState.NotDisplaying);
  });

  it("should hide the alert divs when called", function() {
    Display.showAlert("test", settings);

    Display.hideAlert();

    expect(Display._transitionState).toEqual(TransitionState.ExitTransition);
    expect(alertBackground.classList.contains("hide")).toEqual(true);
    expect(alertBackground.classList.contains("show")).toEqual(false);
    expect(alertText.classList.contains("hide")).toEqual(true);
    expect(alertText.classList.contains("show")).toEqual(false);
  });
});

describe("Display.setAlertLocation", function() {
  var alertContainer, alertBackground, alertText, settings;

  beforeEach(function () {
    document.body.innerHTML = "";
    alertContainer = _createDiv({"class": "alert-container"});
    alertBackground = _createDiv({"id": "alert-background", "class": "hide"});
    alertText = _createDiv({"id": "alert-text", "class": "hide"});
    settings = {
      "location": 1,
      "fontFace": "sans-serif",
      "fontSize": 40,
      "fontColor": "#ffffff",
      "backgroundColor": "#660000",
      "timeout": 5,
      "repeat": 1,
      "scroll": true
    };
  });

  it("should set the correct class when location is top of the page", function () {
    Display.setAlertLocation(0);

    expect(alertContainer.className).toEqual("alert-container top");
  });

  it("should set the correct class when location is middle of the page", function () {
    Display.setAlertLocation(1);

    expect(alertContainer.className).toEqual("alert-container middle");
  });

  it("should set the correct class when location is bottom of the page", function () {
    Display.setAlertLocation(2);

    expect(alertContainer.className).toEqual("alert-container bottom");
  });
});

describe("Display.addAlertToQueue", function () {
  var alertContainer, alertBackground, alertText, settings;

  beforeEach(function () {
    document.body.innerHTML = "";
    alertContainer = _createDiv({"class": "alert-container"});
    alertBackground = _createDiv({"id": "alert-background", "class": "hide"});
    alertText = _createDiv({"id": "alert-text", "class": "hide"});
    settings = {
      "location": 1,
      "fontFace": "sans-serif",
      "fontSize": 40,
      "fontColor": "#ffffff",
      "backgroundColor": "#660000",
      "timeout": 5,
      "repeat": 1,
      "scroll": true
    };
  });

  it("should add an alert to the queue if one is displaying already", function() {
    Display._alerts = [];
    Display._alertState = AlertState.Displaying;
    var alertObject = {text: "Testing alert queue", settings: settings};

    Display.addAlertToQueue("Testing alert queue", settings);

    expect(Display._alerts.length).toEqual(1);
    expect(Display._alerts[0]).toEqual(alertObject);
  });
});

describe("Display.showNextAlert", function () {
  var alertContainer, alertBackground, alertText, settings;

  beforeEach(function () {
    document.body.innerHTML = "";
    alertContainer = _createDiv({"class": "alert-container"});
    alertBackground = _createDiv({"id": "alert-background", "class": "hide"});
    alertText = _createDiv({"id": "alert-text", "class": "hide"});
    settings = {
      "location": 1,
      "fontFace": "sans-serif",
      "fontSize": 40,
      "fontColor": "#ffffff",
      "backgroundColor": "#660000",
      "timeout": 5,
      "repeat": 1,
      "scroll": true
    };
  });

  it("should return null if there are no alerts in the queue", function () {
    Display._alerts = [];
    Display.showNextAlert();

    expect(Display.showNextAlert()).toBeNull();
  });

  it("should call the alert function correctly if there is an alert in the queue", function () {
    Display._alerts.push({text: "Queued Alert", settings: settings});
    spyOn(Display, "showAlert");
    Display.showNextAlert();

    expect(Display.showAlert).toHaveBeenCalled();
    expect(Display.showAlert).toHaveBeenCalledWith("Queued Alert", settings);
  });
});

describe("Display.alertTransitionEndEvent", function() {
  var e = { stopPropagation: function () { } };

  it("should call event.stopPropagation()", function () {
    spyOn(e, "stopPropagation");

    Display.alertTransitionEndEvent(e);

    expect(e.stopPropagation).toHaveBeenCalled();
  });

  it("should set the correct state after EntranceTransition", function() {
    Display._transitionState = TransitionState.EntranceTransition;

    Display.alertTransitionEndEvent(e);

    expect(Display._transitionState).toEqual(TransitionState.NoTransition);
  });

  it("should set the correct state after ExitTransition, call hideAlert() and showNextAlert()", function() {
    spyOn(Display, "hideAlert");
    spyOn(Display, "showNextAlert");
    Display._transitionState = TransitionState.ExitTransition;

    Display.alertTransitionEndEvent(e);

    expect(Display._transitionState).toEqual(TransitionState.NoTransition);
    expect(Display.hideAlert).toHaveBeenCalled();
    expect(Display.showNextAlert).toHaveBeenCalled();
  });
});

describe("Display.alertAnimationEndEvent", function () {
  var e = { stopPropagation: function () { } };

  it("should call the hideAlert method", function() {
    spyOn(Display, "hideAlert");

    Display.alertAnimationEndEvent(e);

    expect(Display.hideAlert).toHaveBeenCalled();
  });
});

describe("Display.setTextSlide", function () {
  beforeEach(function() {
    document.body.innerHTML = "";
    var slides_container = _createDiv({"class": "slides"});
    var footer_container = _createDiv({"class": "footer"});
    Display._slidesContainer = slides_container;
    Display._footerContainer = footer_container;
    Display._slides = {};
  });

  it("should add a new slide", function () {
    var text = "Amazing grace,\nhow sweet the sound";
    spyOn(Display, "reinit");

    Display.setTextSlide(text);

    expect(Display._slides["test-slide"]).toEqual(0);
    expect($(".slides > section > section").length).toEqual(1);
    expect($(".slides > section > section")[0].innerHTML).toEqual(_prepareText(text));
    expect(Display.reinit).toHaveBeenCalled();
  });

  it("should update an existing slide", function () {
    var text = "That saved a wretch\nlike me";
    spyOn(Display, "reinit");
    Display.setTextSlide("Amazing grace,\nhow sweet the sound");

    Display.setTextSlide(text);

    expect(Display._slides["test-slide"]).toEqual(0);
    expect($(".slides > section > section").length).toEqual(1);
    expect($(".slides > section > section")[0].innerHTML).toEqual(_prepareText(text));
    expect(Display.reinit).toHaveBeenCalledTimes(1); // only called once for the first setTextSlide
  });

  it("should give the new slide the future class", function () {
    var text = "That saved a wretch\nlike me";
    spyOn(Display, "reinit");
    Display.setTextSlide("Amazing grace,\nhow sweet the sound");

    Display.setTextSlide(text);

    expect($(".slides > section > section")[0].classList.contains("future")).toEqual(true);
  });
});

describe("Display.setTextSlides", function () {
  beforeEach(function() {
    document.body.innerHTML = "";
    var slides_container = _createDiv({"class": "slides"});
    var footer_container = _createDiv({"class": "footer"});
    Display._slidesContainer = slides_container;
    Display._footerContainer = footer_container;
    Display._slides = {};
  });

  it("should add a list of slides", function () {
    var slides = [
      {
        "verse": "v1",
        "text": "Amazing grace, how sweet the sound\nThat saved a wretch like me\n" +
                "I once was lost, but now I'm found\nWas blind but now I see",
        "footer": "Public Domain"
      },
      {
        "verse": "v2",
        "text": "'twas Grace that taught, my heart to fear\nAnd grace, my fears relieved.\n" +
                "How precious did that grace appear,\nthe hour I first believed.",
        "footer": "Public Domain"
      }
    ];
    spyOn(Display, "clearSlides");
    spyOn(Reveal, "sync");
    spyOn(Reveal, "slide");

    Display.setTextSlides(slides);

    expect(Display.clearSlides).toHaveBeenCalledTimes(0);
    expect(Display._slides["v1"]).toEqual(0);
    expect(Display._slides["v2"]).toEqual(1);
    expect($(".slides > section > section").length).toEqual(2);
    expect(Reveal.sync).toHaveBeenCalledTimes(1);
  });

  it("should correctly set outline width", function () {
    const slides = [
      {
        "verse": "v1",
        "text": "Amazing grace, how sweet the sound\nThat saved a wretch like me\n" +
                "I once was lost, but now I'm found\nWas blind but now I see",
        "footer": "Public Domain"
      }
    ];
    const theme = {
      'font_main_color': 'yellow',
      'font_main_outline': true,
      'font_main_outline_size': 42,
      'font_main_outline_color': 'red'
    };
    spyOn(Reveal, "sync");
    spyOn(Reveal, "slide");

    Display.setTheme(theme);
    Display.setTextSlides(slides);

    const slidesDiv = $(".text-slides")[0];
    expect(slidesDiv.style['text-shadow']).toEqual(_buildTextOutline(42, 'red').join(', '));
  })

  it("should correctly set text alignment,\
      (check the order of alignments in the emuns are the same in both js and python)", function () {
    const slides = [
      {
        "verse": "v1",
        "text": "Amazing grace, how sweet the sound\nThat saved a wretch like me\n" +
                "I once was lost, but now I'm found\nWas blind but now I see",
        "footer": "Public Domain"
      }
    ];
    //
    const theme = {
      'display_horizontal_align': 3,
      'display_vertical_align': 1
    };
    spyOn(Reveal, "sync");
    spyOn(Reveal, "slide");

    Display.setTheme(theme);
    Display.setTextSlides(slides);

    const slidesDiv = $(".text-slides")[0];
    expect(slidesDiv.style['text-align-last']).toEqual('justify');
    expect(slidesDiv.style['justify-content']).toEqual('center');
  })

  it("should enable shadows", function () {
    const slides = [
      {
        "verse": "v1",
        "text": "Amazing grace, how sweet the sound\nThat saved a wretch like me\n" +
                "I once was lost, but now I'm found\nWas blind but now I see",
        "footer": "Public Domain"
      }
    ];
    //
    const theme = {
      'font_main_shadow': true,
      'font_main_shadow_color': "#000",
      'font_main_shadow_size': 5
    };
    spyOn(Reveal, "sync");
    spyOn(Reveal, "slide");

    Display.setTheme(theme);
    Display.setTextSlides(slides);

    const slidesDiv = $(".text-slides")[0];
    expect(slidesDiv.style['text-shadow']).not.toEqual('');
  })

  it("should not enable shadows", function () {
    const slides = [
      {
        "verse": "v1",
        "text": "Amazing grace, how sweet the sound\nThat saved a wretch like me\n" +
                "I once was lost, but now I'm found\nWas blind but now I see",
        "footer": "Public Domain"
      }
    ];
    //
    const theme = {
      'font_main_shadow': false,
      'font_main_shadow_color': "#000",
      'font_main_shadow_size': 5
    };
    spyOn(Reveal, "sync");
    spyOn(Reveal, "slide");

    Display.setTheme(theme);
    Display.setTextSlides(slides);

    const slidesDiv = $(".text-slides")[0];
    expect(slidesDiv.style['text-shadow']).toEqual('');
  })

  it("should correctly set slide size position to theme size when adding a text slide", function () {
    const slides = [
      {
        "verse": "v1",
        "text": "Amazing grace, how sweet the sound\nThat saved a wretch like me\n" +
                "I once was lost, but now I'm found\nWas blind but now I see",
        "footer": "Public Domain"
      }
    ];
    //
    const theme = {
      'font_main_y': 789,
      'font_main_x': 1000,
      'font_main_width': 1230,
      'font_main_height': 4560
    };
    spyOn(Reveal, "sync");
    spyOn(Reveal, "slide");

    Display.setTheme(theme);
    Display.setTextSlides(slides);

    const slidesDiv = $(".text-slides")[0];
    expect(slidesDiv.style['margin-top']).toEqual('789px');
    expect(slidesDiv.style['left']).toEqual('1000px');
    expect(slidesDiv.style['width']).toEqual('1230px');
    expect(slidesDiv.style['height']).toEqual('4560px');
  })
});

describe("Display.setImageSlides", function () {
  beforeEach(function() {
    document.body.innerHTML = "";
    var slides_container = _createDiv({"class": "slides"});
    var footer_container = _createDiv({"class": "footer"});
    Display._slidesContainer = slides_container;
    Display._footerContainer = footer_container;
    Display._slides = {};
  });

  it("should add a list of images", function () {
    var slides = [{"path": "file:///openlp1.jpg"}, {"path": "file:///openlp2.jpg"}];
    spyOn(Reveal, "sync");
    spyOn(Reveal, "slide");

    Display.setImageSlides(slides);

    expect(Display._slides["0"]).toEqual(0);
    expect(Display._slides["1"]).toEqual(1);
    expect($(".slides > section > section").length).toEqual(2);
    expect($(".slides > section > section > img").length).toEqual(2);
    expect($(".slides > section > section > img")[0].getAttribute("src")).toEqual("file:///openlp1.jpg");
    expect($(".slides > section > section > img")[0].getAttribute("style")).toEqual("width: 100%; height: 100%; margin: 0; object-fit: contain;");
    expect($(".slides > section > section > img")[1].getAttribute("src")).toEqual("file:///openlp2.jpg");
    expect($(".slides > section > section > img")[1].getAttribute("style")).toEqual("width: 100%; height: 100%; margin: 0; object-fit: contain;");
    expect(Reveal.sync).toHaveBeenCalledTimes(1);
  });
});

describe("Display.setFullscreenImage", function () {
  beforeEach(function() {
    document.body.innerHTML = "";
    var slides_container = _createDiv({"class": "slides"});
    var footer_container = _createDiv({"class": "footer"});
    Display._slidesContainer = slides_container;
    Display._footerContainer = footer_container;
    Display._slides = {};
  });

  it("should set a fullscreen image", function () {
    var image = "file:///openlp1.jpg";
    let bg_color = "#000";
    spyOn(Reveal, "sync");
    spyOn(Reveal, "slide");

    Display.setFullscreenImage(bg_color, image);

    expect($(".slides > section > img")[0].getAttribute("src")).toEqual("file:///openlp1.jpg");
    expect(Reveal.sync).toHaveBeenCalledTimes(1);
  });
});

describe("Display.setBackgroundImage and Display.resetTheme", function () {
  beforeEach(function() {
    document.body.innerHTML = "";
    var slides_container = _createDiv({"class": "slides"});
    Display._slidesContainer = slides_container;
    var section = document.createElement("section");
    Display._slidesContainer.appendChild(section);
  });

  it("should set the background image data and call sync once for set slides and again for set background", function () {
    spyOn(Reveal, "sync");
    spyOn(Reveal, "slide");

    Display.setBackgroundImage("/file/path");

    expect($(".slides > section")[0].getAttribute("data-background")).toEqual("url('/file/path')");
    expect(Reveal.sync).toHaveBeenCalledTimes(1);
  });

  it("should restore the background image to the theme", function () {
    Display._theme = {
      'background_type': BackgroundType.Image,
      'background_filename': '/another/path'
    };
    $(".slides > section")[0].setAttribute("data-background", "/file/path");
    spyOn(Reveal, "sync");
    spyOn(Reveal, "slide");

    Display.resetTheme();

    expect($(".slides > section")[0].getAttribute("data-background")).toEqual("url('/another/path')");
    expect(Reveal.sync).toHaveBeenCalledTimes(1);
  });
});

describe("Display.setVideo", function () {
  beforeEach(function() {
    document.body.innerHTML = "";
    var slides_container = _createDiv({"class": "slides"});
    Display._slidesContainer = slides_container;
    Display._slides = {};
  });

  it("should add a video to the page", function () {
    var video = {"path": "file:///video.mp4"};
    spyOn(Reveal, "sync");
    spyOn(Reveal, "slide");

    Display.setVideo(video);

    expect($(".slides > section").length).toEqual(1);
    expect($(".slides > section > video").length).toEqual(1);
    expect($(".slides > section > video")[0].src).toEqual("file:///video.mp4")
    expect(Reveal.sync).toHaveBeenCalledTimes(1);
  });
});

describe("Display.playVideo", function () {
  var playCalled = false,
      mockVideo = {
        play: function () {
          playCalled = true;
        }
      };

  beforeEach(function () {
    spyOn(window, "$").and.returnValue([mockVideo]);
  });

  it("should play the video when called", function () {
    Display.playVideo();
    expect(playCalled).toEqual(true);
  });
});

describe("Display.pauseVideo", function () {
  var pauseCalled = false,
      mockVideo = {
        pause: function () {
          pauseCalled = true;
        }
      };

  beforeEach(function () {
    spyOn(window, "$").and.returnValue([mockVideo]);
  });

  it("should pause the video when called", function () {
    Display.pauseVideo();
    expect(pauseCalled).toEqual(true);
  });
});

describe("Display.stopVideo", function () {
  var pauseCalled = false,
      mockVideo = {
        pause: function () {
          pauseCalled = true;
        },
        currentTime: 10.0
      };

  beforeEach(function () {
    spyOn(window, "$").and.returnValue([mockVideo]);
  });

  it("should play the video when called", function () {
    Display.stopVideo();
    expect(pauseCalled).toEqual(true);
    expect(mockVideo.currentTime).toEqual(0.0);
  });
});

describe("Display.seekVideo", function () {
  var mockVideo = {
        currentTime: 1.0
      };

  beforeEach(function () {
    spyOn(window, "$").and.returnValue([mockVideo]);
  });

  it("should seek to the specified position within the video when called", function () {
    Display.seekVideo(7.34);
    expect(mockVideo.currentTime).toEqual(7.34);
  });
});

describe("Display.setPlaybackRate", function () {
  var mockVideo = {
        playbackRate: 1.0
      };

  beforeEach(function () {
    spyOn(window, "$").and.returnValue([mockVideo]);
  });

  it("should set the playback rate of the video when called", function () {
    // Let's sound like chipmunks!
    Display.setPlaybackRate(1.25);
    expect(mockVideo.playbackRate).toEqual(1.25);
  });
});

describe("Display.setVideoVolume", function () {
  var mockVideo = {
        volume: 1.0
      };

  beforeEach(function () {
    spyOn(window, "$").and.returnValue([mockVideo]);
  });

  it("should set the correct volume of the video when called", function () {
    // Make it quiet
    Display.setVideoVolume(30);
    expect(mockVideo.volume).toEqual(0.3);
  });
});

describe("Display.toggleVideoMute", function () {
  var mockVideo = {
        muted: false
      };

  beforeEach(function () {
    spyOn(window, "$").and.returnValue([mockVideo]);
  });

  it("should mute the video when called", function () {
    mockVideo.muted = false;
    Display.toggleVideoMute();
    expect(mockVideo.muted).toEqual(true);
  });

  it("should unmute the video when called", function () {
    mockVideo.muted = true;
    Display.toggleVideoMute();
    expect(mockVideo.muted).toEqual(false);
  });
});
