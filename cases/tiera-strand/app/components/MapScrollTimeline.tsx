'use client';

import { useEffect, useRef, useState } from 'react';

/* ─── Types ─── */
interface Marker {
  id: string;
  lat: number;
  lng: number;
  color: string;
  label: string;
  shortLabel?: string;   // always-visible name tag beneath dot
  labelPos?: 'above' | 'below'; // default 'below'
  pulse?: boolean;
  size?: number;
}

interface MapState {
  center: [number, number];
  zoom: number;
  markers: Marker[];
  routeCoords?: [number, number][];
  routeColor?: string;
  routes?: Array<{ coords: [number, number][]; color: string }>;
  date: string;
  time: string;
}

interface Step {
  id: number;
  act?: string;
  borderColor: string;
  mapState: MapState;
  title: string;
  pills?: Array<{ color: string; label: string }>;
  body: string[];
  details?: string[];
  videoFile?: string;
  videoFiles?: { file: string; label: string }[];
  venuePhoto?: string;
  venueAddress?: string;
  poiCard?: {
    traits: string[];
    behaviors: string[];
  };
}

/* ─── Coordinate constants ─── */
const SIXTH_ST: [number, number]  = [30.2671, -97.7385];
const SHAKESPEARES: [number, number] = [30.2671, -97.7394];
const BLIND_PIG: [number, number]    = [30.2671, -97.7387];
const TRINITY_6TH: [number, number]  = [30.2671, -97.7379];
const MOOSEKNUCKLE: [number, number] = [30.2671, -97.7372];
const BIJOU_LOUNGE: [number, number]  = [30.2673, -97.7348];
const SAN_JAC: [number, number]      = [30.2678, -97.7368];
const I35_CROSS: [number, number]    = [30.2700, -97.7320];
const WENDYS: [number, number]       = [30.2738, -97.7295];
const AUSTIN_CITY: [number, number]  = [30.2672, -97.7431];
const BERGER_RD: [number, number]    = [31.1260, -97.3405];
const OVERVIEW: [number, number]     = [30.69,   -97.54];

/* ─── Shared marker sets ─── */
const sixthStMarkers = (active: string, show: string[] = ['shakespeares','blindpig','trinity','mooseknuckle']): Marker[] => {
  const all: Marker[] = [
    { id: 'shakespeares', lat: SHAKESPEARES[0], lng: SHAKESPEARES[1], color: '#9D4EDD', label: "Shakespeare's Pub – 1:44 AM POI sighting", shortLabel: "Shakespeare's", pulse: active === 'shakespeares', size: active === 'shakespeares' ? 16 : 11 },
    { id: 'blindpig',     lat: BLIND_PIG[0],    lng: BLIND_PIG[1],    color: '#9D4EDD', label: "The Blind Pig – 1:45 AM",                 shortLabel: 'The Blind Pig',  pulse: active === 'blindpig',     size: active === 'blindpig'     ? 16 : 11 },
    { id: 'trinity',      lat: TRINITY_6TH[0],  lng: TRINITY_6TH[1],  color: '#EBE2CD', label: "6th & Trinity (Old School Bar) – ~2:00 AM",shortLabel: 'Old School Bar', pulse: active === 'trinity',      size: active === 'trinity'      ? 16 : 11 },
    { id: 'mooseknuckle', lat: MOOSEKNUCKLE[0], lng: MOOSEKNUCKLE[1], color: '#C04E01', label: "Mooseknuckle Pub – ~2:30 AM altercation",  shortLabel: 'Mooseknuckle',   pulse: active === 'mooseknuckle', size: active === 'mooseknuckle' ? 16 : 11 },
  ];
  return all.filter(m => show.includes(m.id));
};

/* ─── Steps ─── */
const STEPS: Step[] = [
  {
    id: 0,
    borderColor: 'transparent',
    mapState: {
      center: OVERVIEW,
      zoom: 8,
      markers: [
        { id: 'austin', lat: AUSTIN_CITY[0], lng: AUSTIN_CITY[1], color: '#C04E01', label: 'Last seen: Downtown Austin, April 16', shortLabel: 'Austin — Last seen Apr 16', size: 13 },
        { id: 'midpt',  lat: 30.695,         lng: -97.537,         color: '#EBE2CD', label: '~75 miles apart', shortLabel: '~ 75 miles', size: 0 },
        { id: 'berger', lat: BERGER_RD[0],   lng: BERGER_RD[1],   color: '#E63946', label: 'Body found: Berger Rd, Bell County, April 21', shortLabel: 'Bell County — Found Apr 21', size: 13 },
      ],
      routeCoords: [AUSTIN_CITY, BERGER_RD],
      routeColor: '#E63946',
      date: 'APRIL 2023',
      time: '',
    },
    title: '', // title card — handled separately
    body: [],
  },
  {
    id: 1,
    act: 'Act I — The Night Out',
    borderColor: '#C04E01',
    mapState: {
      center: AUSTIN_CITY,
      zoom: 13,
      markers: [
        { id: 'austin', lat: AUSTIN_CITY[0], lng: AUSTIN_CITY[1], color: '#C04E01', label: 'Downtown Austin — 6th Street' },
      ],
      date: 'APRIL 15, 2023',
      time: 'EVENING',
    },
    title: 'Tiera Photographed',
    pills: [{ color: '#C04E01', label: 'TIERA STRAND' }],
    body: [
      'Tiera Strand, 25, goes out with a group of friends to Austin\'s 6th Street entertainment district. A photograph taken this night is the last known image of Tiera alive.',
      'She is described by her family as full of life — bubbly, sassy, expressive. She had plans to finish school and join the Navy. She was a mother to a 6-year-old daughter.',
    ],
  },
  {
    id: 2,
    act: 'Act I — The Night Out',
    borderColor: '#9D4EDD',
    mapState: {
      center: SHAKESPEARES,
      zoom: 19,
      markers: sixthStMarkers('shakespeares', ['shakespeares']),
      date: 'APRIL 16, 2023',
      time: '1:44 AM',
    },
    title: 'POI Captured on Body Cam',
    pills: [{ color: '#9D4EDD', label: 'PERSON OF INTEREST' }],
    body: [
      'Footage screened at APD\'s press conference shows an officer\'s Axon body camera capturing a man on the 300 block of E 6th Street performing what\'s described as a military-style facing movement.',
      'This is the first documented appearance of the Person of Interest (POI) on 6th Street — approximately 45 minutes before he will approach Tiera. The exact venue doorway is unconfirmed; APD has not released the source footage.',
    ],
    details: [
      'Footage source: APD press conference screen capture — original file not publicly released',
    ],
    poiCard: {
      traits: [
        'Broad shoulders, muscular build',
        'Light gray sweatshirt — small chest emblem',
        'Light wash jeans, dark sneakers',
        'Military-style 5A frames glasses',
        'Both ears pierced',
        'Approx. 6\'0", athletic frame',
      ],
      behaviors: [
        'Military-style facing movement at 1:44 AM — suggests military or law enforcement training',
        'Remained on 6th Street ~45 min before approaching Tiera — investigators do not believe this was a random encounter',
        'Conspicuously absent from area during the Mooseknuckle altercation',
        'Made contact only after Tiera was isolated and stripped of her belongings',
        'Chain-smoking began immediately upon contact — not observed smoking at any point before',
      ],
    },
    videoFile: 'poi-shakespeares-144am.mp4',
    venuePhoto: 'shakespeares-pub.jpg',
    venueAddress: "Shakespeare's Pub · 314 E 6th St",
  },
  {
    id: 3,
    act: 'Act I — The Night Out',
    borderColor: '#9D4EDD',
    mapState: {
      center: BLIND_PIG,
      zoom: 19,
      markers: sixthStMarkers('blindpig', ['shakespeares', 'blindpig', 'trinity']),
      routeCoords: [SHAKESPEARES, BLIND_PIG, TRINITY_6TH],
      routeColor: '#9D4EDD',
      date: 'APRIL 16, 2023',
      time: '1:45 AM',
    },
    title: 'Blind Pig Footage',
    pills: [{ color: '#9D4EDD', label: 'PERSON OF INTEREST' }],
    body: [
      'Approximately 40 seconds after the Shakespeare\'s footage, a second Axon clip captures the POI walking past The Blind Pig bar on 6th Street.',
      'The POI continues moving through the 6th Street corridor. He has not yet made contact with Tiera at this point.',
    ],
    videoFile: 'poi-blind-pig-145am.mp4',
    venuePhoto: 'blind-pig.webp',
    venueAddress: 'The Blind Pig · 317 E 6th St',
  },
  {
    id: 4,
    act: 'Act I — The Night Out',
    borderColor: '#EBE2CD',
    mapState: {
      center: TRINITY_6TH,
      zoom: 19,
      markers: sixthStMarkers('trinity', ['shakespeares', 'blindpig', 'trinity']),
      routeCoords: [SHAKESPEARES, BLIND_PIG, TRINITY_6TH],
      routeColor: '#9D4EDD',
      date: 'APRIL 16, 2023',
      time: '~2:00 AM',
    },
    title: 'Trinity Street Confrontation',
    pills: [{ color: '#9D4EDD', label: 'PERSON OF INTEREST' }],
    body: [
      'Surveillance footage from POD146 (6th and Trinity — Old School Bar) shows the POI walking with a group. A woman in the group lunges at him; she is pulled back by friends.',
      'Two unidentified women near a rickshaw also speak with the POI around this time. Law enforcement has sought these individuals for interviews.',
    ],
    videoFile: 'pod146-old-school-bar-200am.mp4',
    venuePhoto: 'old-school-bar.jpg',
    venueAddress: 'Old School Bar · 6th & Trinity St',
  },
  {
    id: 45,
    act: 'Act I — The Night Out',
    borderColor: '#EBE2CD',
    mapState: {
      center: [30.2685, -97.7350] as [number, number],
      zoom: 17,
      markers: [
        ...sixthStMarkers('', ['shakespeares', 'blindpig', 'trinity']),
        { id: 'i35dept', lat: I35_CROSS[0], lng: I35_CROSS[1], color: '#EBE2CD', label: 'POI captured heading east under IH-35 — 2:09 AM', shortLabel: '2:09 AM — IH-35', pulse: true, size: 16 },
      ],
      routes: [
        { coords: [SHAKESPEARES, BLIND_PIG, TRINITY_6TH], color: '#9D4EDD' },
        { coords: [TRINITY_6TH, I35_CROSS], color: '#EBE2CD' },
      ],
      date: 'APRIL 16, 2023',
      time: '2:09 AM',
    },
    title: 'POI Departs Under IH-35',
    pills: [{ color: '#9D4EDD', label: 'PERSON OF INTEREST' }],
    body: [
      'POD102, a camera mounted on the 600 block of IH-35 and facing west, captures the POI walking east under the Interstate 35 overpass at 2:09 AM — moving away from the 6th Street corridor.',
      'This is 9 minutes after his last sighting at the Trinity Street encounter. He will reappear at Mooseknuckle Pub approximately 20 minutes later. What he did in that interval, and how he returned, is not explained by any recovered footage.',
    ],
    details: [
      'Camera: POD102, 600 block IH-35, west-facing',
      'Direction of travel: east — away from 6th Street entertainment district',
      '9 minutes after Trinity Street encounter',
      'Reappears at Mooseknuckle ~20 minutes later — gap unaccounted for',
    ],
    videoFiles: [
      { file: 'pod102-ih35-209am-a.mp4', label: 'CLIP 1 — 2:09:39 AM' },
      { file: 'pod102-ih35-209am-b.mp4', label: 'CLIP 2 — 2:09:50 AM' },
    ],
  },
  {
    id: 5,
    act: 'Act II — The Altercation',
    borderColor: '#C04E01',
    mapState: {
      center: [30.2676, -97.7360] as [number, number],
      zoom: 17,
      markers: [
        ...sixthStMarkers('mooseknuckle', ['shakespeares', 'blindpig', 'trinity', 'mooseknuckle']),
        { id: 'i35ret', lat: I35_CROSS[0], lng: I35_CROSS[1], color: '#EBE2CD', label: 'IH-35 — 2:09 AM departure', shortLabel: 'IH-35 — 2:09 AM', size: 10 },
      ],
      routes: [
        { coords: [SHAKESPEARES, BLIND_PIG, TRINITY_6TH], color: '#9D4EDD' },
        { coords: [TRINITY_6TH, I35_CROSS], color: '#EBE2CD' },
        { coords: [I35_CROSS, MOOSEKNUCKLE], color: '#C04E01' },
      ],
      date: 'APRIL 16, 2023',
      time: '~2:30 AM',
    },
    title: 'Altercation at Mooseknuckle Pub',
    pills: [
      { color: '#C04E01', label: 'TIERA STRAND' },
    ],
    body: [
      'Inside Mooseknuckle Pub at 406 E. 6th Street, a group of girls begin beating Tiera. She is kicked out of the bar. The fight continues outside.',
      'The friends who came with her are present but do not intervene. A witness records the tail end of the fight on a cell phone.',
      'After the incident, Tiera angrily storms off — leaving behind her cell phone, purse, and car keys. She has no way to call for help and no way to pay for transportation.',
    ],
    details: [
      'Assault begins inside the club, continues outside after she is kicked out',
      'Friends present but did not assist — confirmed by witness video',
      'Left without phone, purse, wallet, bank card, car keys',
      'Friends depart in Tiera\'s van without reporting her missing',
      'Family not notified until the following day (April 17)',
    ],
    venuePhoto: 'mooseknuckle.webp',
    venueAddress: 'Mooseknuckle Pub · 406 E 6th St',
  },
  {
    id: 6,
    act: 'Act III — The Last Hours',
    borderColor: '#9D4EDD',
    mapState: {
      center: SAN_JAC,
      zoom: 18,
      markers: [
        ...sixthStMarkers('', ['shakespeares', 'blindpig', 'trinity', 'mooseknuckle']),
        { id: 'sanjac', lat: SAN_JAC[0], lng: SAN_JAC[1], color: '#C04E01', label: 'First contact: POI approaches Tiera', shortLabel: 'First contact', pulse: true, size: 16 },
      ],
      routes: [
        { coords: [SHAKESPEARES, BLIND_PIG, TRINITY_6TH, MOOSEKNUCKLE], color: '#9D4EDD' },
        { coords: [MOOSEKNUCKLE, SAN_JAC], color: '#4A8A7C' },
      ],
      date: 'APRIL 16, 2023',
      time: 'POST-2:30 AM',
    },
    title: 'POI Approaches Tiera',
    pills: [
      { color: '#C04E01', label: 'TIERA STRAND' },
      { color: '#9D4EDD', label: 'PERSON OF INTEREST' },
    ],
    body: [
      'Now alone and without her belongings, Tiera is approached by the POI near San Jacinto. This is the first documented contact between them. They begin walking together, moving away from I-35 and toward San Jacinto.',
      'The POI had been on 6th Street for approximately 45 minutes before this approach. He was not present during the Mooseknuckle altercation. He made contact only after Tiera was isolated and vulnerable.',
    ],
    details: [
      'POI had been observed on 6th Street for ~45 min before this contact',
      'POI was not near Tiera during the earlier altercation',
      'POI approaches only after Tiera is alone and without possessions',
      'Tiera appears comfortable in initial video footage',
    ],
    videoFile: 'poi-tiera-san-jacinto.mp4',
  },
  {
    id: 7,
    act: 'Act III — The Last Hours',
    borderColor: '#9D4EDD',
    mapState: {
      center: I35_CROSS,
      zoom: 17,
      markers: [
        { id: 'sanjac',    lat: SAN_JAC[0],      lng: SAN_JAC[1],      color: '#EBE2CD', label: 'First contact' },
        { id: 'bijou',     lat: BIJOU_LOUNGE[0], lng: BIJOU_LOUNGE[1], color: '#9D4EDD', label: 'Bijou Lounge — horse cam records pair heading NE', shortLabel: 'Bijou Lounge' },
        { id: 'i35cross',  lat: I35_CROSS[0],    lng: I35_CROSS[1],    color: '#9D4EDD', label: 'Direction reversal — heading toward I-35', pulse: true },
      ],
      routes: [
        { coords: [SHAKESPEARES, BLIND_PIG, TRINITY_6TH, MOOSEKNUCKLE, SAN_JAC], color: '#9D4EDD' },
        { coords: [SAN_JAC, BIJOU_LOUNGE, I35_CROSS], color: '#4A8A7C' },
      ],
      date: 'APRIL 16, 2023',
      time: '~2:35 AM',
    },
    title: 'Direction Change',
    pills: [
      { color: '#C04E01', label: 'TIERA STRAND' },
      { color: '#9D4EDD', label: 'PERSON OF INTEREST' },
    ],
    body: [
      'The pair reverses direction, now walking back toward I-35. Horse camera footage (Bijou Lounge to their left) records them moving northeast.',
      'At this point, investigators note the POI begins chain-smoking — a behavior that was not observed during his 45 minutes on 6th Street before meeting Tiera.',
    ],
    details: [
      'Prior to meeting Tiera, POI was not observed smoking at any point',
      'Chain-smoking begins immediately after contact with Tiera',
      'Behavioral change noted as potentially significant by investigators',
    ],
    videoFile: 'horse-cam-bijou-lounge.mp4',
    venuePhoto: 'bijou-lounge.jpg',
    venueAddress: 'Bijou Lounge · ~500 E 6th St',
  },
  {
    id: 8,
    act: 'Act III — The Last Hours',
    borderColor: '#C04E01',
    mapState: {
      center: WENDYS,
      zoom: 17,
      markers: [
        { id: 'sanjac',   lat: SAN_JAC[0],   lng: SAN_JAC[1],   color: '#EBE2CD', label: 'First contact' },
        { id: 'i35cross', lat: I35_CROSS[0], lng: I35_CROSS[1], color: '#EBE2CD', label: 'Direction reversal' },
        { id: 'wendys',   lat: WENDYS[0],    lng: WENDYS[1],    color: '#C04E01', label: "Wendy's parking lot — LAST SIGHTING", pulse: true },
      ],
      routeCoords: [SAN_JAC, I35_CROSS, WENDYS],
      date: 'APRIL 16, 2023',
      time: '2:40 AM',
    },
    title: 'Last Confirmed Sighting',
    pills: [
      { color: '#C04E01', label: 'TIERA STRAND — LAST SIGNAL' },
    ],
    body: [
      'POD145 footage (6th and Brushy) captures the pair crossing under I-35 and walking into a Wendy\'s parking lot north of downtown Austin at 2:40 AM. This is the last recovered footage of Tiera alive.',
      'The Wendy\'s drive-through camera did not capture activity in the parking lot. No witnesses from Wendy\'s staff or customers came forward. No video or physical evidence of what occurred next has been recovered.',
    ],
    details: [
      'Last verified location: Wendy\'s parking lot, north of I-35',
      'Drive-through camera did not cover parking lot area',
      'No witnesses came forward from Wendy\'s',
      'No evidence recovered of what occurred after this point',
    ],
    videoFile: 'pod145-wendys-240am.mp4',
  },
  {
    id: 9,
    act: 'Act IV — Gone',
    borderColor: '#EBE2CD',
    mapState: {
      center: AUSTIN_CITY,
      zoom: 12,
      markers: [
        { id: 'wendys',  lat: WENDYS[0],      lng: WENDYS[1],      color: '#C04E01', label: "Last seen: Wendy's parking lot, 2:40 AM",       shortLabel: "Last seen — Wendy's, 2:40 AM", size: 13 },
        { id: 'austin',  lat: AUSTIN_CITY[0], lng: AUSTIN_CITY[1], color: '#EBE2CD', label: 'Austin PD — Missing person report filed April 17', shortLabel: 'APD report filed — Apr 17',        size: 13, labelPos: 'above' },
      ],
      date: 'APRIL 17, 2023',
      time: 'DAYTIME',
    },
    title: 'Missing Person Report Filed',
    body: [
      'The friends who left Tiera on 6th Street finally contact her family the following day. When the family tried to reach Tiera, the friends answered her phone and said they had her belongings — which the family says is completely out of character for Tiera.',
      'Tiera\'s family immediately reports her missing to the Austin Police Department. But by this point, Tiera has been missing for approximately 14 hours.',
      '"She would not have gone to that area without someone that knows and loves her," said Tiera\'s aunt, Jordaya Dorris.',
    ],
    details: [
      'Family tried to call — friends answered Tiera\'s phone',
      'Friends said they had her belongings — family said this was out of character',
      'APD missing persons report filed April 17',
      'Approximately 14 hours had passed since her last sighting',
    ],
    venuePhoto: 'tiera-strand-flyer.webp',
    venueAddress: 'Missing Person — Tiera Strand · Filed April 17, 2023',
  },
  {
    id: 10,
    act: 'Act V — Found',
    borderColor: '#E63946',
    mapState: {
      center: [30.68, -97.54],
      zoom: 8,
      markers: [
        { id: 'austin',  lat: WENDYS[0],      lng: WENDYS[1],      color: '#C04E01', label: "Last seen: Austin, April 16 at 2:40 AM" },
        { id: 'berger',  lat: BERGER_RD[0],   lng: BERGER_RD[1],   color: '#E63946', label: 'Body found: 1300 block of Berger Rd, north of Temple', pulse: true },
      ],
      routeCoords: [WENDYS, BERGER_RD],
      date: 'APRIL 21, 2023',
      time: 'MORNING',
    },
    title: 'Body Discovered — Bell County',
    pills: [{ color: '#E63946', label: 'BELL COUNTY, TX' }],
    body: [
      'Heavy rain on Thursday night (April 20) washes roadside grass flat. A citizen driving to work the next morning discovers Tiera\'s body in a ditch at the 1300 block of Berger Road, just north of Temple — approximately 75 miles from where she was last seen in Austin.',
      'Tiera\'s family has confirmed she had no known connection to Bell County. There is no reason she would have traveled there voluntarily — without her belongings, without someone she knew.',
      '"She would not have gone to that area without someone that knows and loves her." — Jordaya Dorris, aunt',
    ],
    details: [
      '75 miles north of Austin on the I-35 corridor',
      'No known connection to Bell County — family confirms',
      'Body in advanced decomposition (~5 days exposure)',
      'Rain runoff exposed body by washing down roadside grass',
      'Partial DNA profile recovered but not CODIS-eligible',
      'Investigation opened as homicide by Bell County Sheriff\'s Department',
    ],
    venuePhoto: 'body-found-kdhnews.jpg',
    venueAddress: 'Scene — 1300 block Berger Rd, Bell County · Photo: KDH News',
  },
  {
    id: 11,
    act: 'Act V — Found',
    borderColor: '#EBE2CD',
    mapState: {
      center: BERGER_RD,
      zoom: 13,
      markers: [
        { id: 'berger', lat: BERGER_RD[0], lng: BERGER_RD[1], color: '#E63946', label: '1300 block Berger Rd — Bell County', pulse: true },
      ],
      date: 'JULY 27, 2023',
      time: '',
    },
    title: 'Autopsy: Cause of Death Undetermined',
    body: [
      'An autopsy performed by the Dallas County Medical Examiner rules the cause of death as "undetermined." The report notes no visible trauma to the body, but acknowledges that the level of decomposition may have obscured fatal injuries.',
      '"The events that occurred between the time the decedent was last known alive and the time her remains were discovered are currently unknown. Furthermore, the level of decomposition may have obscured an injury or injuries that caused or contributed to her death." — Autopsy report',
      'The investigation continues to be treated as a homicide by the Bell County Sheriff\'s Department and the Austin Police Department Homicide Unit.',
    ],
    details: [
      'Cause of death classified as "undetermined"',
      'No visible trauma noted on remains',
      'Decomposition likely obscured cause of fatal injury',
      'Investigation treated as homicide — case remains active',
      'Numerous individuals questioned; no definitive suspects named',
    ],
  },
  {
    id: 12,
    act: 'Act V — Found',
    borderColor: '#4A8A7C',
    mapState: {
      center: [30.68, -97.54],
      zoom: 8,
      markers: [
        { id: 'austin', lat: WENDYS[0],    lng: WENDYS[1],    color: '#C04E01', label: 'Last seen: Austin, April 16' },
        { id: 'berger', lat: BERGER_RD[0], lng: BERGER_RD[1], color: '#E63946', label: 'Found: Bell County, April 21' },
      ],
      routeCoords: [WENDYS, BERGER_RD],
      routeColor: '#4A8A7C',
      date: '2023 — PRESENT',
      time: '',
    },
    title: 'The Investigation',
    pills: [
      { color: '#4A8A7C', label: 'CASE ACTIVE' },
    ],
    body: [
      'The Bell County Sheriff\'s Office Criminal Investigations Division and the Austin Police Department Homicide Unit are jointly investigating Tiera\'s death. The case is classified as a homicide.',
      'A partial DNA profile was recovered from evidence but does not meet the threshold for CODIS database matching. Investigators are exploring whether the profile qualifies for Investigative Genetic Genealogy (IGG) — the same technique used to identify the Golden State Killer.',
      'The Person of Interest captured on multiple surveillance cameras on the night of April 15–16 has never been publicly identified. Investigators believe someone in the public knows who he is.',
    ],
    details: [
      'Partial DNA profile recovered — not CODIS-eligible at current threshold',
      'IGG (investigative genetic genealogy) being evaluated as next step',
      'POI appears on APD body cam, Axon footage, and multiple private cameras',
      'POI physical description: broad shoulders, muscular build, light gray sweatshirt with small chest emblem, light wash jeans, dark sneakers, military-style 5A frames glasses, both ears pierced',
      'BCSD CID: 254-933-5442',
      'APD Homicide: 512-472-8477',
    ],
  },
  {
    id: 13,
    act: 'If You Were There',
    borderColor: '#EBE2CD',
    mapState: {
      center: SIXTH_ST,
      zoom: 16,
      markers: [
        { id: 'shakespeares', lat: SHAKESPEARES[0], lng: SHAKESPEARES[1], color: '#9D4EDD', label: "Shakespeare's Pub",  shortLabel: "Shakespeare's", size: 11 },
        { id: 'blindpig',     lat: BLIND_PIG[0],    lng: BLIND_PIG[1],    color: '#9D4EDD', label: 'The Blind Pig',      size: 11 },
        { id: 'trinity',      lat: TRINITY_6TH[0],  lng: TRINITY_6TH[1],  color: '#EBE2CD', label: 'Old School Bar',     size: 11 },
        { id: 'mooseknuckle', lat: MOOSEKNUCKLE[0], lng: MOOSEKNUCKLE[1], color: '#C04E01', label: 'Mooseknuckle Pub',   shortLabel: 'Mooseknuckle', size: 11 },
      ],
      routeCoords: [SHAKESPEARES, BLIND_PIG, TRINITY_6TH, MOOSEKNUCKLE],
      routeColor: '#9D4EDD',
      date: 'APRIL 15–16, 2023',
      time: '',
    },
    title: 'Were You on 6th Street That Night?',
    body: [
      'If you were on Austin\'s 6th Street in the early hours of April 16, 2023 — near Shakespeare\'s Pub, The Blind Pig, the Old School Bar, or Mooseknuckle Pub — you may have seen something that could break this case open.',
      'Investigators are specifically looking for anyone who saw the altercation at Mooseknuckle Pub around 2:30 AM, witnessed Tiera after she was separated from her group, or recognized the Person of Interest.',
      'Tiera\'s daughter is growing up without her mother. Her family deserves answers. No detail is too small.',
    ],
    details: [
      'Bell County Sheriff\'s Office CID: 254-933-5442',
      'Austin Police Department Homicide: 512-472-8477',
      'Tips can be submitted anonymously',
      'Any information — even if you\'re unsure it matters — could help',
    ],
  },
];

/* ─── Component ─── */
export function MapScrollTimeline() {
  const mapRef      = useRef<HTMLDivElement>(null);
  const leafletRef  = useRef<any>(null);
  const routeRef    = useRef<any>(null);
  const markersRef  = useRef<Map<string, any>>(new Map());
  const narrativeRef = useRef<HTMLDivElement>(null);

  const [activeStep, setActiveStep] = useState(0);
  const [selectedVideo, setSelectedVideo] = useState<string | null>(null);
  const [selectedPhoto, setSelectedPhoto] = useState<{ src: string; address: string } | null>(null);
  const [clockDate, setClockDate] = useState('APRIL 2023');
  const [clockTime, setClockTime] = useState('');

  /* ── Init Leaflet ── */
  useEffect(() => {
    if (!mapRef.current) return;

    let map: any = null;

    const init = async () => {
      await import('leaflet/dist/leaflet.css');
      const L = (await import('leaflet')).default;

      // Guard against StrictMode double-invoke
      if ((mapRef.current as any)._leaflet_id) return;

      map = L.map(mapRef.current!, {
        center: OVERVIEW,
        zoom: 8,
        zoomControl: true,
        attributionControl: true,
      });

      L.tileLayer(
        'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        {
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
          subdomains: 'abcd',
          maxZoom: 20,
        }
      ).addTo(map);

      leafletRef.current = map;
      await renderMapState(L, map, STEPS[0].mapState);
    };

    init();

    return () => {
      if (map) {
        map.remove();
        leafletRef.current = null;
        markersRef.current.clear();
        routeRef.current = null;
      }
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  /* ── Map state renderer ── */
  const renderMapState = async (L: any, map: any, state: MapState): Promise<void> => {
    // Clear existing markers
    markersRef.current.forEach(m => map.removeLayer(m));
    markersRef.current.clear();

    // Clear route(s)
    if (routeRef.current) {
      if (Array.isArray(routeRef.current)) {
        routeRef.current.forEach((r: any) => map.removeLayer(r));
      } else {
        map.removeLayer(routeRef.current);
      }
      routeRef.current = null;
    }

    const routeStyle = { weight: 2.5, opacity: 0.75, dashArray: '7 5' };

    // Draw multiple named routes
    if (state.routes && state.routes.length > 0) {
      routeRef.current = state.routes.map(r =>
        L.polyline(r.coords, { ...routeStyle, color: r.color }).addTo(map)
      );
    } else if (state.routeCoords && state.routeCoords.length > 1) {
      routeRef.current = L.polyline(state.routeCoords, {
        ...routeStyle,
        color: state.routeColor ?? '#4A8A7C',
      }).addTo(map);
    }

    // Add markers
    state.markers.forEach(m => {
      const size = m.size ?? 12;
      const half = size / 2;

      const wrapper = document.createElement('div');
      wrapper.style.cssText = 'display:flex;flex-direction:column;align-items:center;gap:3px;';

      const dot = document.createElement('div');
      dot.style.cssText = `
        width:${size}px;height:${size}px;border-radius:50%;
        background:${m.color};
        border:2px solid rgba(255,255,255,0.6);
        box-shadow:0 0 8px ${m.color}aa;
        cursor:pointer;flex-shrink:0;
      `;
      if (m.pulse) dot.classList.add('pulse-marker');

      const labelAbove = m.shortLabel && m.labelPos === 'above';

      if (m.shortLabel) {
        const tag = document.createElement('div');
        tag.style.cssText = `
          font-family:'IBM Plex Mono',monospace;font-size:9px;
          color:#EBE2CD;letter-spacing:0.04em;white-space:nowrap;
          background:rgba(6,11,20,0.82);
          padding:2px 5px;border-radius:2px;
          border:1px solid rgba(244,229,196,0.15);
          pointer-events:none;
        `;
        tag.textContent = m.shortLabel;
        if (labelAbove) {
          wrapper.appendChild(tag);
          wrapper.appendChild(dot);
        } else {
          wrapper.appendChild(dot);
          wrapper.appendChild(tag);
        }
      } else {
        wrapper.appendChild(dot);
      }

      const iconH = size + (m.shortLabel ? 22 : 0);
      // For labelAbove, anchor at bottom of icon (dot is at bottom); for below, anchor at top half (dot at top)
      const iconAnchorY = labelAbove ? iconH - half : half;
      const icon = L.divIcon({
        html: wrapper,
        className: '',
        iconSize: [100, iconH],
        iconAnchor: [50, iconAnchorY],
      });

      const marker = L.marker([m.lat, m.lng], { icon })
        .bindPopup(`<span style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#D8DADB">${m.label}</span>`, {
          closeButton: false,
          maxWidth: 280,
        })
        .addTo(map);

      markersRef.current.set(m.id, marker);
    });

    // Fly to new center
    map.flyTo(state.center, state.zoom, { duration: 1.2, easeLinearity: 0.4 });
  };

  /* ── Update map on step change ── */
  useEffect(() => {
    if (!leafletRef.current) return;
    const step = STEPS.find(s => s.id === activeStep);
    if (!step) return;

    const update = async () => {
      const L = (await import('leaflet')).default;
      renderMapState(L, leafletRef.current, step.mapState);

      setClockDate(step.mapState.date);
      setClockTime(step.mapState.time);
    };
    update();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeStep]);

  /* ── Scroll tracking ── */
  useEffect(() => {
    const narrative = narrativeRef.current;
    if (!narrative) return;

    const stepEls = narrative.querySelectorAll<HTMLElement>('[data-step]');

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const id = parseInt(entry.target.getAttribute('data-step') || '0');
            setActiveStep(id);
            // Update left border color
            stepEls.forEach(el => el.classList.remove('is-active'));
            entry.target.classList.add('is-active');
          }
        });
      },
      { root: narrative, threshold: 0.35, rootMargin: '-10% 0px -35% 0px' }
    );

    stepEls.forEach(el => observer.observe(el));

    // Progress bar
    const onScroll = () => {
      const { scrollTop, scrollHeight, clientHeight } = narrative;
      const pct = (scrollTop / (scrollHeight - clientHeight)) * 100;
      const bar = document.getElementById('progress-bar');
      if (bar) bar.style.width = `${Math.min(pct, 100)}%`;
    };

    narrative.addEventListener('scroll', onScroll, { passive: true });

    return () => {
      observer.disconnect();
      narrative.removeEventListener('scroll', onScroll);
    };
  }, []);

  /* ── Border color for active step ── */
  const activeBorderColor = STEPS.find(s => s.id === activeStep)?.borderColor ?? 'transparent';

  return (
    <>
      <div id="progress-bar" />

      {/* Nav */}
      <nav className="case-nav">
        <div className="nav-title">Tiera Strand</div>
        <span className="nav-badge">ACTIVE CASE</span>
        <span className="nav-tip">BCSD CID 254-933-5442 · APD 512-472-8477</span>
      </nav>

      {/* Clock */}
      <div id="clock">
        <div className="clock-date">{clockDate}</div>
        {clockTime && <div className="clock-time">{clockTime}</div>}
      </div>

      {/* Map */}
      <div id="map" ref={mapRef} />

      {/* Narrative */}
      <div id="narrative" ref={narrativeRef}>

        {/* Title card (step 0) */}
        <div
          className="step title-card"
          data-step={0}
          style={{ borderLeftColor: 'transparent' }}
        >
          <div className="case-dateline">April 2023 — Austin, Texas</div>
          <div className="step-title">The Disappearance &amp;<br />Death of Tiera Strand</div>
          <p className="step-subtitle">
            On the night of April 15–16, 2023, Tiera Strand, 25, went out with friends to Austin's 6th Street. She was beaten at a bar, left without her phone or wallet, and encountered an unknown man. She was never seen alive again. Five days later her body was found in a ditch 75 miles away.
          </p>

          <div className="title-stats">
            <div className="stat-box">
              <div className="stat-label">Last Seen</div>
              <div className="stat-value">Apr. 16 at 2:40 AM</div>
            </div>
            <div className="stat-box">
              <div className="stat-label">Found</div>
              <div className="stat-value">Apr. 21 in Bell County</div>
            </div>
            <div className="stat-box">
              <div className="stat-label">Distance</div>
              <div className="stat-value">75 miles</div>
            </div>
            <div className="stat-box">
              <div className="stat-label">Case Status</div>
              <div className="stat-value" style={{ color: '#C04E01' }}>UNSOLVED</div>
            </div>
          </div>
          <div className="scroll-hint">↓ Scroll to begin</div>
        </div>

        {/* Remaining steps */}
        {STEPS.slice(1).map(step => (
          <div
            key={step.id}
            data-step={step.id}
            className="step"
            style={{ borderLeftColor: activeStep === step.id ? step.borderColor : 'transparent' }}
          >
            {step.act && <div className="step-act">{step.act}</div>}
            <div className="step-time">{step.mapState.time || step.mapState.date}</div>
            <div className="step-title">{step.title}</div>

            {step.pills && (
              <div style={{ marginBottom: '4px' }}>
                {step.pills.map(pill => (
                  <span key={pill.label} className="person-pill">
                    <span className="pill-dot" style={{ background: pill.color }} />
                    {pill.label}
                  </span>
                ))}
              </div>
            )}

            {step.body.map((para, i) => (
              <p key={i}>{para}</p>
            ))}

            {step.details && step.details.length > 0 && (
              <ul className="step-details">
                {step.details.map((d, i) => <li key={i}>{d}</li>)}
              </ul>
            )}

            {/* POI profile card */}
            {step.poiCard && (
              <div className="poi-card">
                <div className="poi-card-label">◈ Person of Interest — Physical Description</div>
                <div className="poi-trait-grid">
                  {step.poiCard.traits.map((t, i) => (
                    <div key={i} className="poi-trait">{t}</div>
                  ))}
                </div>
                <div className="poi-card-label">◈ Investigator Notes</div>
                {step.poiCard.behaviors.map((b, i) => (
                  <div key={i} className="poi-behavior">{b}</div>
                ))}
              </div>
            )}

            {/* Venue photo thumbnail */}
            {step.venuePhoto && (
              <button
                className="venue-thumb"
                onClick={() => setSelectedPhoto({ src: step.venuePhoto!, address: step.venueAddress ?? '' })}
              >
                <img
                  src={`/venues/${step.venuePhoto}`}
                  alt={step.venueAddress}
                  className="venue-thumb-img"
                  onError={e => { (e.currentTarget.parentElement as HTMLElement).style.display = 'none'; }}
                />
                <div className="venue-thumb-overlay">
                  <span className="venue-thumb-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="13" height="13">
                      <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
                    </svg>
                  </span>
                  <span>{step.venueAddress}</span>
                </div>
              </button>
            )}

            {step.videoFile && (
              <button
                className="video-btn"
                onClick={() => setSelectedVideo(step.videoFile || null)}
              >
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M8 5v14l11-7z" />
                </svg>
                View video →
              </button>
            )}

            {step.videoFiles && step.videoFiles.map((v, i) => (
              <button
                key={i}
                className="video-btn"
                onClick={() => setSelectedVideo(v.file)}
              >
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M8 5v14l11-7z" />
                </svg>
                {v.label}
              </button>
            ))}

            {/* Tip contacts on last step */}
            {step.id === 11 && (
              <div className="tip-contacts">
                <p><strong>BCSD CID:</strong> 254-933-5442</p>
                <p><strong>APD Tip Line:</strong> 512-472-8477</p>
                <p style={{ marginTop: '8px' }}><em>"We will do everything in our power to make sure these people pay for what they did." — Jordaya Dorris, aunt</em></p>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Photo lightbox */}
      {selectedPhoto && (
        <div className="video-overlay" onClick={() => setSelectedPhoto(null)}>
          <div className="photo-panel" onClick={e => e.stopPropagation()}>
            <button className="video-close" onClick={() => setSelectedPhoto(null)}>✕</button>
            <img
              src={`/venues/${selectedPhoto.src}`}
              alt={selectedPhoto.address}
              style={{ width: '100%', display: 'block', maxHeight: '78vh', objectFit: 'cover' }}
            />
            <div className="video-filename" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="13" height="13" style={{ color: 'var(--c-tiera)', flexShrink: 0 }}>
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/>
              </svg>
              <span>{selectedPhoto.address}</span>
              <span style={{ marginLeft: 'auto', opacity: 0.45 }}>Street-level reference · Google Maps</span>
            </div>
          </div>
        </div>
      )}

      {/* Video modal */}
      {selectedVideo && (
        <div className="video-overlay" onClick={() => setSelectedVideo(null)}>
          <div className="video-panel" onClick={e => e.stopPropagation()}>
            <button className="video-close" onClick={() => setSelectedVideo(null)}>✕</button>
            <video
              src={`/videos/${selectedVideo}`}
              controls
              autoPlay
              style={{ width: '100%', display: 'block', maxHeight: '72vh' }}
            />
            <div className="video-filename">{selectedVideo}</div>
          </div>
        </div>
      )}
    </>
  );
}
