#!/usr/bin/env node
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
const root = dirname(fileURLToPath(import.meta.url));
const csv = readFileSync(join(root, 'shipbuilding_facilities.csv'), 'utf8');
const row = csv.split(/\r?\n/).find((l) => l.startsWith('ARC-SHIP-071,'));
if (!row) throw new Error('ARC-SHIP-071 missing');
if (!row.includes('68.680715')) throw new Error('expected densified lat 68.680715*');
if (!row.includes('17.118896')) throw new Error('expected densified lon 17.118896*');
if (!row.includes('gis-densify-1312')) throw new Error('missing gis-densify-1312 tag');
if (!row.includes('9016226127')) throw new Error('missing OSM node/9016226127');
console.log('OK ARC-SHIP-071 Grovfjord densify lock');
