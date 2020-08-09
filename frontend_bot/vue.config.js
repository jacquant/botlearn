const CompressionPlugin = require("compression-webpack-plugin");

module.exports = {
  publicPath: process.env.FRONT_BOT_HOST,
  transpileDependencies: ["vuetify"],
  configureWebpack: {
    plugins: [
      new CompressionPlugin({
        filename: "[path].gz[query]",
        algorithm: "gzip",
        test: /\.js$|\.css$|\.html$/,
        threshold: 10240,
        minRatio: 0.8,
      }),
      new CompressionPlugin({
        filename: "[path].br[query]",
        algorithm: "brotliCompress",
        test: /\.(js|css|html|svg)$/,
        compressionOptions: {
          level: 11,
        },
        threshold: 10240,
        minRatio: 0.8,
      })
    ],
    optimization: {
      splitChunks: {
        chunks: "initial",
        minSize: 10000,
        maxSize: 200000,
      },
    }
  },
};
