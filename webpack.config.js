const path = require("path");
const webpack = require("webpack");
const BundleTracker = require("webpack-bundle-tracker");
const { CleanWebpackPlugin } = require('clean-webpack-plugin');


const PRJ_PATH = path.resolve(__dirname, 'project');


let mode = 'development';
mode = (process.env.NODE_ENV !== undefined) ? process.env.NODE_ENV : mode;


module.exports = {
  mode: mode,
  context: __dirname,
  devtool: 'source-map',
  entry: {
    users: path.resolve(PRJ_PATH, "users/static/js/index.js"),
  },
  output: {
    path: path.resolve(PRJ_PATH, "frontend", "dist"),
    filename: "[name]-[fullhash].js",
    publicPath: 'http://0.0.0.0:9000/static/dist/'
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      }
    ]
  },
  plugins: [
    new webpack.ProgressPlugin(),
    new CleanWebpackPlugin({root: PRJ_PATH, verbose: true}),
    new BundleTracker({
      path: path.resolve(PRJ_PATH, "frontend", "dist"),
      filename: 'webpack-stats.json'
    }),
  ]
}