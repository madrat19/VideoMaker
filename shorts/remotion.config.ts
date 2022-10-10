import {Config} from 'remotion';
import {webpackOverride} from './src/webpack-override';

Config.Rendering.setImageFormat('jpeg');
Config.Output.setOverwriteOutput(true);
// Config.Rendering.setScale(2/3);

Config.Bundling.overrideWebpackConfig(webpackOverride);
