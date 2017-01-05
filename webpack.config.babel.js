import _ from 'lodash';
import path from 'path';
import webpack from 'webpack';
import HappyPack from 'happypack';
import fs from 'fs-extra';

import DummyPlugin from './scripts/build/webpackDummyPlugin.js';
import DummyOutputPlugin from './scripts/build/webpackDummyOutputPlugin.js';
import ExtractTextPlugin from 'extract-text-webpack-plugin';
import CopyWebpackPlugin from 'copy-webpack-plugin';
import postcssAutoprefixerPlugin from 'autoprefixer';
import stylusRupturePlugin from 'rupture';

import responsiveCutoff from './anubis/ui/responsive.inc.js';

const extractProjectCSS = new ExtractTextPlugin({ filename: 'anubis.css', allChunks: true });
const extractVendorCSS = new ExtractTextPlugin({ filename: 'vendors.css', allChunks: true });

function root(fn) {
  return path.resolve(__dirname, fn);
}

function ResponsivePlugin() {
  return style => {
    style.define('responsiveCutoff', responsiveCutoff, true);
  };
}

export default function (env = {}) {
  const config = {
    context: root('anubis/ui'),
    devtool: 'source-map',
    watchOptions: {
      aggregateTimeout: 1000,
    },
    entry: {
      anubis: './Entry.js',
    },
    output: {
      path: root('anubis/.static_build'),
      publicPath: '/',    // overwrite in entry.js
      filename: '[name].js',
      chunkFilename: '[name].chunk.js',
    },
    resolve: {
      modules: [root('node_modules'), root('anubis/ui')],
      extensions: ['.js', ''],
    },
    module: {
      preLoaders: [
        {
          test: /\.js?$/,
          loader: 'eslint',
          exclude: /node_modules\//,
        }
      ],
      loaders: [
        {
          // fonts
          test: /\.(svg|ttf|eot|woff|woff2)$/,
          loader: 'file',
          query: {
            name: '[path][name].[ext]?[sha512:hash:base62:7]',
          },
        },
        {
          // images
          test: /\.(png|jpg)$/,
          loader: 'url',
          query: {
            limit: 4024,
            name: '[path][name].[ext]?[sha512:hash:base62:7]',
          }
        },
        {
          // ES2015 scripts
          test: /\.js$/,
          exclude: /node_modules\//,
          loader: 'babel',
          query: {
            ...require('./package.json').babelForProject,
            cacheDirectory: !_.isError(_.attempt(() => fs.ensureDirSync(root('.cache/babel'))))
              ? root('.cache/babel')
              : false,
          },
          happy: { id: 'js' },
        },
        {
          // fix pickadate loading
          test: /pickadate/,
          loader: 'imports',
          query: { define: '>false' },
        },
        {
          // project stylus stylesheets
          test: /\.styl$/,
          loader: env.watch
            ? ['style', 'css', 'postcss', 'stylus?resolve url']
            : extractProjectCSS.extract(['css', 'postcss', 'stylus?resolve url'])
            ,
        },
        {
          // vendors stylesheets
          test: /\.css$/,
          include: /node_modules\//,
          loader: env.watch
            ? ['style', 'css']
            : extractVendorCSS.extract(['css'])
            ,
        },
        {
          // project stylesheets
          test: /\.css$/,
          exclude: /node_modules\//,
          loader: env.watch
            ? ['style', 'css']
            : extractProjectCSS.extract(['css', 'postcss'])
            ,
        },
      ],
    },
    plugins: [
      env.watch
        ? new DummyPlugin()
        : new HappyPack({
            id: 'js',
            tempDir: root('.cache/happypack'),
          })
        ,

      new webpack.ProvidePlugin({
        $: 'jquery',
        jQuery: 'jquery',
        'window.jQuery': 'jquery',
        katex: 'katex',
      }),

      // don't include locale files in momentjs
      new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),

      // extract stylesheets into a standalone file
      env.watch
        ? new DummyOutputPlugin('vendors.css')
        : extractVendorCSS
        ,

      env.watch
        ? new DummyOutputPlugin('anubis.css')
        : extractProjectCSS
        ,

      // extract 3rd-party JavaScript libraries into a standalone file
      env.watch
        ? new DummyOutputPlugin('vendors.js')
        : new webpack.optimize.CommonsChunkPlugin({
            name: 'vendors',
            filename: 'vendors.js',
            minChunks: (module, count) => (
              module.resource
              && module.resource.indexOf(root('anubis/ui/')) === -1
              && module.resource.match(/\.js$/)
            ),
          })
        ,

      // copy static assets
      new CopyWebpackPlugin([{ from: root('anubis/ui/static') }]),

      // copy emoji images
      new CopyWebpackPlugin([{ from: root('node_modules/emojify.js/dist/images/basic'), to: 'img/emoji/' }]),

    ],
    postcss: () => [postcssAutoprefixerPlugin],
    stylus: {
      use: [
        ResponsivePlugin(),
        stylusRupturePlugin(),
      ],
      import: [
        '~common/common.inc.styl',
      ]
    },
    eslint: {
      configFile: root('anubis/ui/.eslintrc.yml'),
    },
    stats: {
      children: false,
    },
  };

  return config;
};
