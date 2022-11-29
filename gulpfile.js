const gulp = require("gulp");
const rename = require("gulp-rename");
const webpack = require("webpack-stream");

gulp.task('javascript', function() {
  return gulp
    .src("./hip/static/js/webpack_entry.js")
    .pipe(webpack(require("./webpack.config.js")))
    .pipe(rename("main.js"))
    .pipe(gulp.dest("./hip/static/js/bundles/"));
});

gulp.task('watch-js', function(done) {
  gulp.watch(["./hip/static/js/*.js"], gulp.series("javascript"));
  done();
})

gulp.task('styles', function() {
  const sass = require('gulp-sass')(require('sass'));
  return gulp
    .src("./hip/static/styles/bundle.scss")
    .pipe(sass().on('error', sass.logError))
    .pipe(rename("bundle.css"))
    .pipe(gulp.dest("./static/styles/"));
});

gulp.task('watch-css', function(done) {
  gulp.watch(
    [
    './hip/static/styles/bundle.scss',
    './hip/static/styles/**/*.scss'
    ], gulp.series('styles')
  );
  done();
});


exports.default = gulp.series('styles', 'javascript', 'watch-css', 'watch-js');
