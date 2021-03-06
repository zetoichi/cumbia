const path = require("path");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const exclusions = /node_modules/;

module.exports = [
  {
    mode: 'development',
    entry: {
      app: "./core/static/src/js/app.js",
    },
    output: {
      path: path.resolve(__dirname, "core/static/dist"),
      publicPath: "/static/",
      filename: "bundle.js",
      chunkFilename: "[id]-[chunkhash].js",
      clean: true
    },
    devtool: 'inline-source-map',
    devServer: {
      port: 8081,
      writeToDisk: true,
    },
    module: {
      rules: [
        {
          test: /\.html$/i,
          loader: 'html-loader',
        },
        {
          test: /\.css$/,
          exclude: exclusions,
          use: [
            MiniCssExtractPlugin.loader,
            { loader: "css-loader" },
          ],
        },
      ],
    },
    resolve: {
      alias: {
        'hamburgers': path.resolve(__dirname, "node_modules/hamburgers/dist/hamburgers.css")
      }  
    },
    plugins: [
      new CleanWebpackPlugin({ cleanStaleWebpackAssets: false }),
      new MiniCssExtractPlugin(),
    ],
  },
];