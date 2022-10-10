import {Composition} from 'remotion';
import {MyComposition} from './Composition';
import './style.css';
import data from '../public/post.json';

const MAX_DURATION = 59;
export const fps = 60;
const width = 1080;
const height = 1920;

let durationInSeconds = 0;
let numberOfComments = 0;

calculateDuration();
durationInSeconds = Math.ceil(durationInSeconds);

const durationInFrames = durationInSeconds * fps;

export const RemotionVideo = () => {
  return (
    <>
      <Composition
        id="MyComp"
        component={MyComposition}
        durationInFrames={durationInFrames}
        fps={fps}
        width={width}
        height={height}
        defaultProps={{data, numberOfComments}}
      />
    </>
  );
};

function calculateDuration() {
  if (Number(data.title_audio_file_lenght) > MAX_DURATION) {
    durationInSeconds = 59;
    return false;
  }
  durationInSeconds = Number(data.title_audio_file_lenght);

  if (data.selftext) {
    let postDuration = 0;
    for (const part of data.selftext) {
      postDuration += Number(part.length);
    }
    if (durationInSeconds + postDuration <= MAX_DURATION) {
      durationInSeconds += postDuration;
    } else {
      durationInSeconds = 59;
      return false;
    }
  }

  if (data.comments) {
    for (const comment of data.comments) {
      let commentDuration = 0;
      for (const part of comment.body) {
        commentDuration += Number(part.length);
      }
      if (durationInSeconds + commentDuration <= MAX_DURATION) {
        durationInSeconds += commentDuration;
        numberOfComments++;
      } else {
        return true;
      }
    }
  }
}
