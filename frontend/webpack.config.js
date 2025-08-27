const path = require('path'); // Node module to handle file paths
const HtmlWebpackPlugin = require('html-webpack-plugin'); // Generates index.html with your bundle

module.exports = {
  // Entry point of your app
  entry: './src/index.js',

  // Output bundle location
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
    clean: true, // Cleans old builds before generating new ones
  },

  // Development server configuration
  devServer: {
    static: {
      directory: path.join(__dirname, 'public'), // Serve static files from public folder
    },
    compress: true,      // Enable gzip compression
    port: 3000,          // Port number for dev server
    open: true,          // Automatically open browser
    hot: true,           // Enable hot module replacement
    historyApiFallback: true, // <--- add this line

  },

  // Module rules for handling different file types
  module: {
    rules: [
      {
        test: /\.js$/,          // For all .js files
        exclude: /node_modules/, // Ignore node_modules
        use: {
          loader: 'babel-loader', // Use Babel to transpile JS
        },
      },
      {
        test: /\.css$/i,       // For all .css files
        use: ['style-loader', 'css-loader'], // Inject CSS into DOM
      },
    ],
  },

  // Plugins
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html', // Use your public/index.html as template
      filename: 'index.html',
    }),
  ],

  // Enable source maps for easier debugging
  devtool: 'inline-source-map',

  // Mode can be 'development' or 'production'
  mode: 'development',
};
