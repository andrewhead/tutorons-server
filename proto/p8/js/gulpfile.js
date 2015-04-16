var gulp = require('gulp'),
    notify = require('gulp-notify'),
    plumber = require('gulp-plumber'),
    config = require('./config');

function errorHandler() {
  return plumber({
    errorHandler: notify.onError('Error: <%= error.message %>')
  });
}

gulp.task('default', ['build']);
gulp.task('build', ['static', 'compass', 'browserify']);

gulp.task('static', function() {
  return gulp.src(config.globs.other, { base: './src' })
    .pipe(errorHandler())
    .pipe(gulp.dest(config.buildRoot));
});

gulp.task('markup', ['compass'], function() {
  var wrap = require('gulp-wrap'),
      path = require('path'),
      fs = require('fs');

  return gulp.src(config.globs.html, { base: './src' })
    .pipe(errorHandler())
    .pipe(wrap({ src: config.templateFile }, {
      date: new Date().toISOString(),
      title: function() {
        var root = path.join(this.file.cwd, this.file.base),
            file = path.relative(root, this.file.history[0]);

        return config.titles[file] || config.titles['_'];
      },
      svgStyles: fs.readFileSync(path.join(config.compass.css, 'svg.css'), {
        encoding: 'utf-8'
      })
    }))
    .pipe(gulp.dest(config.buildRoot));
});

gulp.task('compass', function() {
  var compass = require('gulp-compass');

  return gulp.src(config.globs.sass)
    .pipe(errorHandler())
    .pipe(compass(config.compass));
});

gulp.task('browserify', function() {
  var browserify = require('browserify'),
      tap = require('gulp-tap');

  return gulp.src('./src/js/javascript.js', { read: false })
    .pipe(errorHandler())
    .pipe(tap(function(file) {
      var bundler = browserify(config.browserify);

      config.browserify.prebundle(bundler);

      bundler.add(file.path);

      file.contents = bundler.bundle();
    }))
    .pipe(gulp.dest(config.buildPath('js')));
});
