#!/usr/bin/env node
// Programmatic TWA project bootstrap — bypasses bubblewrap CLI's interactive wizard.
// Uses @bubblewrap/core directly with all values pre-supplied.

import { createRequire } from 'node:module';
import path from 'node:path';

const require = createRequire(import.meta.url);
const CORE = '/Users/qnc/.nvm/versions/node/v24.15.0/lib/node_modules/@bubblewrap/cli/node_modules/@bubblewrap/core';
const { TwaManifest } = require(`${CORE}/dist/lib/TwaManifest.js`);
const { TwaGenerator } = require(`${CORE}/dist/lib/TwaGenerator.js`);
const { ConsoleLog } = require(`${CORE}/dist/lib/Log.js`);

const TARGET_DIR = '/Users/qnc/Projects/quantumcube/android';
const PWA_MANIFEST_URL = 'https://quantumcube.app/manifest.json';
const KEYSTORE_PATH = path.join(TARGET_DIR, 'quantumcube.keystore');
const TWA_MANIFEST_PATH = path.join(TARGET_DIR, 'twa-manifest.json');

const log = new ConsoleLog('build-twa');

const twaManifest = await TwaManifest.fromWebManifest(PWA_MANIFEST_URL);

twaManifest.packageId = 'app.quantumcube.twa';
twaManifest.host = 'quantumcube.app';
twaManifest.name = 'Quantum Cube';
twaManifest.launcherName = 'Quantum Cube';
twaManifest.startUrl = '/app';
// theme/nav/background colors come pre-populated as Color objects from fromWebManifest — don't overwrite
twaManifest.iconUrl = 'https://quantumcube.app/qc-icon-512.png';
twaManifest.maskableIconUrl = 'https://quantumcube.app/qc-icon-512-maskable.png';
twaManifest.appVersionName = '1.0.0';
twaManifest.appVersion = 1;
twaManifest.appVersionCode = 1;
twaManifest.signingKey = { path: KEYSTORE_PATH, alias: 'quantumcube' };
twaManifest.minSdkVersion = 21;
twaManifest.targetSdkVersion = 35;
twaManifest.fallbackType = 'customtabs';
twaManifest.orientation = 'portrait';
twaManifest.enableNotifications = false;
twaManifest.fingerprints = twaManifest.fingerprints || [];
twaManifest.shortcuts = [];

const validationError = twaManifest.validate();
if (validationError) {
  console.error('TWA manifest invalid:', validationError);
  process.exit(1);
}

console.log('Generating TWA project at:', TARGET_DIR);
const generator = new TwaGenerator();
await generator.createTwaProject(TARGET_DIR, twaManifest, log);

await twaManifest.saveToFile(TWA_MANIFEST_PATH);
console.log('TWA manifest saved to:', TWA_MANIFEST_PATH);
console.log('Done.');
