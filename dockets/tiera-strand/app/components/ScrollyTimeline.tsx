'use client';

import { useEffect, useRef, useState } from 'react';
import { Play, MapPin, Clock } from 'lucide-react';

interface TimelineEvent {
  id: number;
  time: string;
  title: string;
  description: string;
  location?: string;
  videoFile?: string;
  details?: string[];
  importance: 'high' | 'medium' | 'low';
}

const events: TimelineEvent[] = [
  {
    id: 1,
    time: 'April 15, 2023',
    title: 'Tiera Photographed',
    description: 'Last known photo taken of Tiera',
    importance: 'high',
  },
  {
    id: 2,
    time: '1:44 AM – April 16',
    title: 'POI Captured on Body Cam',
    location: '6th Street, Austin',
    description: 'POI captured in front of Shakespeare\'s Pub performing military facing movement',
    videoFile: '(1) 2023-04-16 01.44.52 AM – 0500 Axon Body 3 X60A9348B (in front of Shakespeare\'s Pub).mp4',
    details: [
      'Broad shoulders, muscular build',
      'Light gray sweatshirt with small chest emblem',
      'Light wash jeans, dark sneakers',
      'Military-issue 5A frames glasses',
      'Both ears pierced',
    ],
    importance: 'high',
  },
  {
    id: 3,
    time: '1:45 AM',
    title: 'Blind Pig Footage',
    location: '6th Street, Austin',
    description: 'POI walking past The Blind Pig (second Axon clip, ~40 seconds later)',
    videoFile: '(2) 2023-04-16 01.45.32 AM – 0500 Axon Body 3 X60A9348B walking past The Blind Pig (to his left).mp4',
    importance: 'high',
  },
  {
    id: 4,
    time: '~2:00 AM',
    title: 'Trinity Street Confrontation',
    location: 'Trinity Street (between 6th and 7th)',
    description: 'POI seen walking with group; woman lunges at him, pulled back by friends. Persons of interest sought for identification.',
    videoFile: '(5) POD146 6th and Trinity Old School Bar – 04.16.2023 2.00.06.309 AM.mov',
    importance: 'high',
  },
  {
    id: 5,
    time: '~2:30 AM',
    title: 'Altercation at Mooseknuckle Pub',
    location: 'Mooseknuckle Pub, 406 E. 6th Street',
    description: 'Tiera becomes separated from her friend group following an altercation that starts inside the club. Multiple girls beat her; she is kicked out and the fight continues outside. She leaves with no phone, purse, bank card, money, or car keys—everything taken or left behind. The friends who came with her do not help her during the incident. After leaving angrily, her friends drive her van home without reporting her missing.',
    details: [
      'Assault begins inside the club by other patrons',
      'Fight continues outside after she is kicked out',
      'Multiple girls involved in beating',
      'Left defenseless without possessions, including phone and car keys',
      'Friends who attended with her present but did not assist',
      'Friends left 6th Street in Tiera\'s van without alerting authorities or family',
      'Witness cell phone video recorded—shows tail end of fight and friends not helping',
      'Family not notified until the next day (April 17)',
      'Tiera angrily storms off alone after the incident'
    ],
    importance: 'high',
  },
  {
    id: 6,
    time: 'Post-2:30 AM',
    title: 'POI Approaches Tiera',
    location: 'Downtown Austin (6th Street area)',
    description: 'Tiera, now alone and separated from her friend group, is approached by the POI. This is the first documented contact between them. They begin walking together away from I-35 toward San Jacinto.',
    details: [
      'POI had been observed on 6th Street for ~45 minutes before this contact',
      'POI was NOT near Tiera during the earlier altercation',
      'POI approaches only after Tiera is alone and vulnerable',
      'Tiera appears comfortable in initial video footage'
    ],
    videoFile: '(6) POI walking with Tiera from San Jacinto towards the interstate.mp4',
    importance: 'high',
  },
  {
    id: 7,
    time: '~2:20 AM',
    title: 'Direction Change',
    location: 'San Jacinto / I-35 area',
    description: 'POI and Tiera reverse direction, now walking back toward I-35. POI begins chain-smoking (not observed smoking before meeting Tiera).',
    details: [
      'Prior to meeting Tiera, POI was not observed smoking',
      'Chain-smoking begins immediately after contact with Tiera',
      'Behavior change noted as potentially significant'
    ],
    videoFile: '(7) Horse cam — POI and Tiera walking towards the interstate (Bijou Lounge to their left).mov',
    importance: 'high',
  },
  {
    id: 8,
    time: '2:40 AM',
    title: 'Last Confirmed Sighting',
    location: 'Wendy\'s parking lot, North Austin',
    description: 'POI and Tiera cross under I-35, walk onto sidewalk, then into Wendy\'s parking lot north of downtown. Last recovered footage of Tiera alive.',
    details: [
      'Wendy\'s drive-through camera did not capture parking lot activity',
      'No witnesses came forward from Wendy\'s staff or customers',
      'Time gap of unknown duration between this sighting and discovery',
      'No video or evidence recovered of what occurred next'
    ],
    videoFile: '(8) POD145 6th and Brushy Encore SW – 04.16.2023 2.40.48.965 AM.mov',
    importance: 'high',
  },
  {
    id: 9,
    time: 'April 17, 2023',
    title: 'Missing Person Report Filed',
    location: 'Family reported to authorities',
    description: 'Tiera\'s friends finally inform her family that she is missing. The family reports Tiera as a missing person to law enforcement. This is approximately 14 hours after she was last seen, and 4 days before her body is discovered.',
    details: [
      'Friends waited until next day to alert family',
      'Family immediately reported her missing to Austin Police Department',
      'Initial search begins, but Tiera is no longer in downtown Austin',
      'Case begins to receive media attention'
    ],
    importance: 'high',
  },
  {
    id: 10,
    time: 'April 21, 2023',
    title: 'Body Discovered',
    location: '1300 block of Berger Rd, north of Temple, Bell County (~75 miles from Austin)',
    description: 'Heavy rain Thursday night (April 20) washes roadside grass. Citizen driving to work discovers Tiera\'s body approximately 5 days after last sighting. Autopsy later ruled cause of death as "undetermined," with decomposition potentially obscuring fatal injuries.',
    details: [
      'Body found in ditch at 1300 block of Berger Rd, just north of Temple',
      'Approximately 75 miles from where she was last seen in downtown Austin',
      'Body in advanced decomposition—approximately 5 days exposure',
      'Decomposition level may have obscured fatal injuries or trauma',
      'Rain runoff exposed body by washing grass down roadside',
      'July 2023 autopsy ruled cause of death as "undetermined"',
      'Suggests POI may have familiarity with Bell County area',
      'Partial DNA profile recovered but not CODIS-eligible'
    ],
    importance: 'high',
  },
  {
    id: 11,
    time: 'July 27, 2023',
    title: 'Autopsy Results Released',
    location: 'Dallas County Medical Examiner',
    description: 'The medical examiner\'s autopsy report is released to media. Cause of death is ruled "undetermined." The report indicates no visible trauma to the body, but notes that advanced decomposition may have obscured fatal injuries. The investigation remains open as a homicide.',
    details: [
      'Cause of death classified as "undetermined"',
      'No visible trauma noted on remains',
      'Decomposition may have hidden injuries that caused or contributed to death',
      'Family confirms being attacked by multiple people before disappearance',
      'Family insists she would not have traveled to Bell County voluntarily',
      'Investigation continues to be treated as homicide',
      'Friends initially answered her phone and claimed to have her belongings'
    ],
    importance: 'high',
  },
];

export function ScrollyTimeline() {
  const [visibleIds, setVisibleIds] = useState<Set<number>>(new Set());
  const [selectedVideo, setSelectedVideo] = useState<string | null>(null);
  const observerRefs = useRef<Map<number, IntersectionObserver>>(new Map());

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const id = parseInt(entry.target.getAttribute('data-id') || '0');
            setVisibleIds((prev) => new Set(prev).add(id));
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -100px 0px' }
    );

    const elements = document.querySelectorAll('[data-scrolly-item]');
    elements.forEach((el) => {
      observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  return (
    <div className="min-h-screen" style={{ background: 'var(--grad-dark)' }}>
      {/* Header */}
      <div className="sticky top-0 z-50 backdrop-blur border-b" style={{ backgroundColor: 'rgba(6, 11, 20, 0.95)', borderColor: 'var(--border-subtle)' }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl sm:text-4xl font-bold" style={{ color: 'var(--text-pure)' }}>Tiera Strand</h1>
          <p className="mt-1" style={{ color: 'var(--text-label)' }}>Investigative Timeline — Case Active</p>
        </div>
      </div>

      {/* Timeline Container */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Timeline Events */}
          <div className="lg:col-span-2">
            {events.map((event, index) => (
              <div
                key={event.id}
                data-scrolly-item
                data-id={event.id}
                className={`mb-12 transition-all duration-700 ${
                  visibleIds.has(event.id)
                    ? 'opacity-100 translate-y-0'
                    : 'opacity-0 translate-y-8'
                }`}
              >
                {/* Timeline Marker */}
                <div className="flex gap-6">
                  {/* Vertical Line */}
                  <div className="relative">
                    <div className="w-1 h-full" style={{ background: 'var(--grad-spine)' }} />
                    <div
                      className="absolute top-0 -left-2.5 w-6 h-6 rounded-full border-4 transition-all"
                      style={{
                        borderColor: 'var(--surface-base)',
                        backgroundColor: visibleIds.has(event.id) ? 'var(--accent)' : 'var(--surface-2)',
                        boxShadow: visibleIds.has(event.id) ? '0 0 12px var(--accent)' : 'none'
                      }}
                    />
                  </div>

                  {/* Content Card */}
                  <div className="pb-8 flex-1">
                    <div className="border rounded-lg p-5 transition-all relative" style={{
                      backgroundColor: 'var(--surface-1)',
                      borderColor: 'var(--border-subtle)',
                      borderTop: '3px solid transparent'
                    }} onMouseEnter={(e) => {
                      e.currentTarget.style.backgroundColor = 'var(--surface-2)';
                      e.currentTarget.style.transform = 'translateY(-2px)';
                      e.currentTarget.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.3)';
                    }} onMouseLeave={(e) => {
                      e.currentTarget.style.backgroundColor = 'var(--surface-1)';
                      e.currentTarget.style.transform = 'translateY(0)';
                      e.currentTarget.style.boxShadow = 'none';
                    }}>
                      {/* Gradient top border */}
                      <div style={{
                        position: 'absolute',
                        top: '-3px',
                        left: '0',
                        right: '0',
                        height: '3px',
                        background: 'var(--grad-g03)',
                        borderRadius: '8px 8px 0 0',
                        pointerEvents: 'none'
                      }} />
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <Clock className="w-4 h-4" style={{ color: 'var(--accent)' }} />
                            <p className="text-sm font-mono" style={{ color: 'var(--accent)' }}>{event.time}</p>
                          </div>
                          <h3 className="text-lg sm:text-xl font-bold mb-2" style={{ color: 'var(--text-pure)' }}>
                            {event.title}
                          </h3>
                          {event.location && (
                            <div className="flex items-center gap-2 mb-3">
                              <MapPin className="w-4 h-4" style={{ color: 'var(--text-label)' }} />
                              <p className="text-sm font-semibold" style={{ color: 'var(--text-label)' }}>
                                {event.location}
                              </p>
                            </div>
                          )}
                          <p className="mb-3" style={{ color: 'var(--text-secondary)' }}>{event.description}</p>

                          {/* Details List */}
                          {event.details && event.details.length > 0 && (
                            <ul className="space-y-1 mb-4 pl-4 border-l-2" style={{ borderColor: 'var(--border-mid)' }}>
                              {event.details.map((detail, i) => (
                                <li
                                  key={i}
                                  className="text-sm list-disc list-inside"
                                  style={{ color: 'var(--text-muted)' }}
                                >
                                  {detail}
                                </li>
                              ))}
                            </ul>
                          )}

                          {/* Video Indicator */}
                          {event.videoFile && (
                            <button
                              onClick={() => setSelectedVideo(event.videoFile || null)}
                              className="inline-flex items-center gap-2 px-3 py-2 rounded text-sm border cursor-pointer transition-all hover:scale-105"
                              style={{
                                backgroundColor: 'var(--accent-dim)',
                                color: 'var(--accent)',
                                borderColor: 'var(--accent-border)',
                                border: '1px solid var(--accent-border)'
                              }}>
                              <Play className="w-4 h-4" />
                              View video →
                            </button>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Sidebar - Case Summary */}
          <div className="lg:col-span-1">
            <div className="sticky top-24 border rounded-lg p-6 space-y-6 relative" style={{
              backgroundColor: 'var(--surface-1)',
              borderColor: 'var(--border-subtle)',
              borderLeft: '3px solid transparent'
            }}>
              {/* Gradient left border */}
              <div style={{
                position: 'absolute',
                left: '-3px',
                top: '-1px',
                bottom: '-1px',
                width: '3px',
                background: 'linear-gradient(to bottom, #D8DADB, #C04E01)',
                borderRadius: '12px 0 0 12px',
                pointerEvents: 'none'
              }} />
              <div>
                <h3 className="font-bold mb-2" style={{ color: 'var(--text-pure)' }}>Case Status</h3>
                <p className="text-sm mb-2" style={{ color: 'var(--text-secondary)' }}>
                  Active homicide investigation — Bell County Sheriff's CID and Austin Police Department Homicide Unit
                </p>
                <p className="text-sm italic" style={{ color: 'var(--text-muted)' }}>
                  "We are doing everything in our power to make sure you are held accountable, because justice needs to be served." — Aunt Jordaya Dorris
                </p>
              </div>

              <div>
                <h3 className="font-bold mb-2" style={{ color: 'var(--text-pure)' }}>About Tiera</h3>
                <p className="text-sm mb-3" style={{ color: 'var(--text-secondary)' }}>
                  Mother to a 6-year-old daughter. Full of life, bubbly, sassy, and expressive. She had plans to finish school and pursue her dream of joining the Navy.
                </p>
                <p className="text-sm italic" style={{ color: 'var(--text-muted)' }}>
                  "She was very confident. She was sure of the things she wanted in life. She had plans. She had a future." — Aunt Jordaya Dorris
                </p>
              </div>

              <div>
                <h3 className="font-bold mb-2" style={{ color: 'var(--text-pure)' }}>POI Description</h3>
                <ul className="text-sm space-y-1" style={{ color: 'var(--text-secondary)' }}>
                  <li>• Muscular, broad-shouldered build</li>
                  <li>• Very short faded hair</li>
                  <li>• Both ears pierced</li>
                  <li>• Military-style glasses (5A frames)</li>
                  <li>• Military demeanor / bearing</li>
                </ul>
              </div>

              <div>
                <h3 className="font-bold mb-2" style={{ color: 'var(--text-pure)' }}>Timeline Span</h3>
                <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                  <strong>Last Seen:</strong> April 16, 2:40 AM (Downtown Austin)
                  <br />
                  <strong>Found:</strong> April 21, 2023 (Bell County, 75 miles away)
                  <br />
                  <strong>Exposure:</strong> ~5 days
                  <br />
                  <strong>No connection to Bell County area</strong>
                </p>
              </div>

              <div className="pt-4" style={{ borderTop: '1px solid var(--border-subtle)' }}>
                <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
                  <strong>BCSD CID:</strong> 254-933-5442
                  <br />
                  <strong>APD Tip Line:</strong> 512-472-8477
                  <br />
                  <strong>Email:</strong> sheriff.tips@bellcounty.texas.gov
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Video Modal */}
      {selectedVideo && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          style={{ backgroundColor: 'rgba(0, 0, 0, 0.75)' }}
          onClick={() => setSelectedVideo(null)}
        >
          <div
            className="relative w-full max-w-4xl rounded-lg overflow-hidden"
            style={{ backgroundColor: 'var(--surface-base)' }}
            onClick={(e) => e.stopPropagation()}
          >
            {/* Close Button */}
            <button
              onClick={() => setSelectedVideo(null)}
              className="absolute top-4 right-4 z-10 w-8 h-8 flex items-center justify-center rounded"
              style={{ backgroundColor: 'rgba(0, 0, 0, 0.5)', color: 'var(--text-pure)' }}
            >
              ✕
            </button>

            {/* Video Player */}
            <div className="w-full bg-black">
              <video
                src={`/videos/${selectedVideo}`}
                controls
                autoPlay
                className="w-full h-auto"
                style={{ maxHeight: '70vh' }}
              />
            </div>

            {/* Video Title */}
            <div className="p-4 border-t" style={{ borderColor: 'var(--border-subtle)' }}>
              <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                {selectedVideo}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
