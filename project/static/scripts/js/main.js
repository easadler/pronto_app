(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);throw new Error("Cannot find module '"+o+"'")}var f=n[o]={exports:{}};t[o][0].call(f.exports,function(e){var n=t[o][1][e];return s(n?n:e)},f,f.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
/** @jsx React.DOM */
var SetIntervalMixin = {
  componentWillMount: function() {
    this.intervals = [];
  },
  setInterval: function() {
    this.intervals.push(setInterval.apply(null, arguments));
  },
  componentWillUnmount: function() {
    this.intervals.map(clearInterval);
  }
};

var Circle = React.createClass({displayName: "Circle",
    mixins: [SetIntervalMixin], 
    getDefaultProps: function() {
        return {
            r: 0,
            fill: 'green',
            cx: 0,
            cy: 0,
            opacity: 0.6
        }
    },
    
    getInitialState: function() {
      return {
        milliseconds: 0,
        r: 0
      };
    },
    
    shouldComponentUpdate: function(nextProps) {
      return this.props.r !== this.state.r;
    },
    
    componentWillMount: function() {
      console.log('will mount');
    },
    
    componentWillReceiveProps: function(nextProps) {
      this.setState({milliseconds: 0, r: this.props.r});
    this.setState({fill: this.props.fill});

    },
    
    componentDidMount: function() {
      this.setInterval(this.tick, 10);
    },
    
    tick: function(start) {
      this.setState({milliseconds: this.state.milliseconds + 10});
    },
    
    render: function() {
      var easyeasy = d3.ease('back-out');
      var r = this.state.r + (this.props.r - this.state.r) * easyeasy(Math.min(1, this.state.milliseconds/1000));

      var fill = this.state.fill
        return (
      React.createElement("circle", {
                cx: this.props.cx, 
                cy: this.props.cy, 
                r: r, 
                fill: 'green', 
                opacity: this.props.opacity}
           )
        );
    },
});

var Path = React.createClass({displayName: "Path", 
    render: function() {
      var d = this.props.d
        return (
      React.createElement("path", {
                d: d, 
                fill: 'black'}
           )
        );
    },
});

var Hood = React.createClass({displayName: "Hood",
  getDefaultProps: function() {
    return {
      hoods: []
    }
  },

  shouldComponentUpdate: function(nextProps) {
      return this.props.hoods !== nextProps.hoods;
  },

  render: function() {
    var hoods = this.props.hoods;

    var pathGenerator = this.props.pathGenerator;

    var paths = hoods.map(function(hood,i) {
      return (
  React.createElement(Path, {
     d: pathGenerator(hood), 
      key: i})
      )
    });

    return (
          React.createElement("g", null, paths)
    );
  }
}); 


var Terminal = React.createClass({displayName: "Terminal",
  getDefaultProps: function() {
    return {
      terminals: []
    }
  },

  shouldComponentUpdate: function(nextProps) {
      return this.props.terminals !== nextProps.terminals;
  },

  render: function() {
    var terminals = this.props.terminals;
    var projection = this.props.projection;

    var circles = terminals.map(function(terminal, i) {
      var fill = 'green';
      var size = +terminal.bikes_avail
      var coord = [+terminal.long,+terminal.lat]
      return (
  React.createElement(Circle, {
      cx: projection(coord)[0], 
      cy: projection(coord)[1], 
      r: size, 
      fill: fill, 
      opacity: 0.6, 
      key: terminal.terminal})
      )
    });

    return (
          React.createElement("g", null, circles)
    );
  }
}); 



var Map = React.createClass({displayName: "Map",
    render: function() {
        return (
            React.createElement("svg", {width: this.props.width, 
                 height: this.props.height}, 
              this.props.children
            )
        );
    }
});


App = React.createClass({displayName: "App",
  getDefaultProps: function() {
    return {
      width: 960,
      height: 700
    };
  },

  getInitialState: function() {
    return {
      hoods: [],
      terminals: [],
    };
  },

  componentWillMount: function() {
    var cmp = this;
        var hoods = '{{hoods|safe}}';
        cmp.setProps({
          hoods: topojson.feature(hoods,hoods.objects.Seattle).features
        });
        cmp.setState({
          terminals: '{{terminals|safe}}'
        });
  },


  render: function() {
    var cmp = this;

    var svg = React.DOM.svg;

  var projection = d3.geo.albers()
      .scale( 450000 )
      .rotate( [122.335167,0] )
      .center( [0, 47.608013] )
      .translate( [590/2,1000/2] );

    var counties = this.state.counties
    var terminals = this.state.terminals

    var pathGenerator = d3.geo.path().projection(projection);

    return (React.createElement(Map, {width: this.props.width, 
                  height: this.props.height}, 
              React.createElement(Hood, {hoods: this.props.hoods, pathGenerator: pathGenerator}), 
              React.createElement(Terminal, {terminals: this.state.terminals, 
                projection: projection})
            ));
}

});

React.render(
  React.createElement(App, null),
  document.getElementById('main'));

},{}]},{},[1])