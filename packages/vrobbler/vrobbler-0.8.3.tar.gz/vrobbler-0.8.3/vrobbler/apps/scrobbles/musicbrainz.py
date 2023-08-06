import musicbrainzngs


def lookup_album_from_mb(musicbrainz_id: str) -> dict:
    release_dict = {}

    musicbrainzngs.set_useragent('vrobbler', '0.3.0')
    release_data = musicbrainzngs.get_release_by_id(
        musicbrainz_id,
        includes=['artists', 'release-groups', 'recordings'],
    ).get('release')

    if not release_data:
        return release_dict

    primary_artist = release_data.get('artist-credit')[0]
    release_dict = {
        'artist': {
            'name': primary_artist.get('name'),
            'musicbrainz_id': primary_artist.get('id'),
        },
        'album': {
            'name': release_data.get('title'),
            'musicbrainz_id': musicbrainz_id,
            'musicbrainz_releasegroup_id': release_data.get(
                'release-group'
            ).get('id'),
            'musicbrainz_albumaritist_id': primary_artist.get('id'),
            'year': release_data.get('year')[0:4],
        },
    }

    release_dict['tracks'] = []
    for track in release_data.get('medium-list')[0]['track-list']:
        recording = track['recording']
        release_dict['tracks'].append(
            {
                'title': recording['title'],
                'musicbrainz_id': recording['id'],
                'run_time_ticks': track['length'],
            }
        )

    return release_dict
