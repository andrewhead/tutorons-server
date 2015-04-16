import Snap from 'snapsvg';
import _ from 'lodash';

import util from './util.js';
import javascript from './javascript/parser.js';
import ParserState from './javascript/parser_state.js';

export default class Parser {
  constructor(container, options) {
    this.options = options || {};
    _.defaults(this.options, {
      keepContent: false
    });

    this.container = container;

    this.state = new ParserState(this.container.querySelector('.progress div'));
  }

  set container(cont) {
    this._container = cont;
    this._container.innerHTML = [
      document.querySelector('#svg-container-base').innerHTML,
      this.options.keepContent ? this.container.innerHTML : ''
    ].join('');
    this._addClass('svg-container');
  }

  get container() {
    return this._container;
  }

  _addClass(className) {
    this.container.className = _(this.container.className.split(' '))
      .union([className])
      .value()
      .join(' ');
  }

  _removeClass(className) {
    this.container.className = _(this.container.className.split(' '))
      .without(className)
      .value()
      .join(' ');
  }

  parse(expression) {
    this._addClass('loading');

    return util.tick().then(() => {
      javascript.Parser.SyntaxNode.state = this.state;

      this.parsed = javascript.parse(expression.replace(/\n/g, '\\n'));
      return this;
    });
  }

  render() {
    var svg = Snap(this.container.querySelector('svg'));

    return this.parsed.render(svg.group())
      .then(result => {
        var box = result.getBBox();

        result.transform(Snap.matrix()
          .translate(10 - box.x, 10 - box.y));
        svg.attr({
          width: box.width + 20,
          height: box.height + 20
        });
      })
      .then(() => {
        this._removeClass('loading');
        this.container.removeChild(this.container.querySelector('.progress'));
      });
  }

  cancel() {
    this.state.cancelRender = true;
  }

  get warnings() {
    return this.state.warnings;
  }
}

window.Parser = Parser;
window.showRegex = function(container, pattern) {

    if (!Boolean(document.getElementById('svg-container-base'))) {

        var script = document.createElement("script");
        script.id = "svg-container-base";
        var svgDiv = document.createElement("div");
        svgDiv.className = "svg";
        var svg = document.createElement("svg");
        svgDiv.appendChild(svg);
        script.appendChild(svgDiv);

        var progDiv = document.createElement("div");
        progDiv.className = "progress";
        var innerDiv = document.createElement("div");
        innerDiv.style.width = 0;
        progDiv.appendChild(innerDiv);
        script.appendChild(progDiv);

        document.head.appendChild(script);

    }

    var renderDiv;
    if (!Boolean(document.getElementsByClassName('results').length)) {
        var resDiv = document.createElement("div");
        resDiv.className = "results";
        resDiv.style.display = "block";
        renderDiv = document.createElement("div");
        renderDiv.id = "regexp-render";
        renderDiv.style.display = "block";
        resDiv.appendChild(renderDiv);
        container.appendChild(resDiv);
    } else {
        renderDiv = document.getElementById("regexp-render");
    }

    var parser = new Parser(renderDiv, {});
    parser.parse(pattern).then(parser => { 
        parser.render();
    });
    
}   
