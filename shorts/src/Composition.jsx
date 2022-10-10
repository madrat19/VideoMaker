/* eslint-disable camelcase */
import {useMemo} from 'react';
import {Img, random, Series, Audio} from 'remotion';
import {AbsoluteFill, OffthreadVideo, staticFile} from 'remotion';
import {fps} from './Video';

const BETWEEN = 0;
const SECONDS_IN_VIDEO = 4784;

const Card = ({children}) => {
  return (
    <div className="bg-zinc-800 bg-opacity-80 px-6 py-8 rounded-3xl m-4 z-50 w-full h-fit my-auto">
      {children}
    </div>
  );
};

const Title = ({
  author,
  title,
  time_ago,
  title_audio_file,
  ups,
  subreddit_name,
  subreddit_logo_file,
  num_comments,
  selftext,
  last,
  first,
}) => {
  return (
    <div className="flex gap-4">
      {first ? (
        <div className="flex flex-col items-center justify-centerimage.png gap-2">
          <Img
            className="invert w-20 h-16 opacity-60"
            src={staticFile('/icons/arrow.png')}
          />
          <p className="text-4xl font-semibold">{ups}</p>
          <Img
            className="invert w-20 h-16 rotate-180 opacity-60"
            src={staticFile('/icons/arrow.png')}
          />
        </div>
      ) : (
        <div className="w-20 flex-none" />
      )}
      <div className="flex flex-col gap-4">
        {first && (
          <div className="flex gap-2">
            <Img
              className="rounded-full w-12 h-12"
              src={staticFile(`/${subreddit_logo_file}.png`)}
            />
            <p className="font-semibold">{subreddit_name}</p>
            <p className="opacity-60">•</p>
            <p className="opacity-60 truncate">Posted by {author}</p>
            <p className="opacity-60 truncate">{time_ago}</p>
          </div>
        )}
        {first ? (
          <p className="text-5xl font-semibold">{title}</p>
        ) : (
          <p className="text-5xl">{selftext}</p>
        )}
        {last && (
          <div className="flex items-center justify-start gap-8 opacity-60 relative right-2">
            <div className="flex items-center gap-4 relative right-2">
              <Img
                className="invert w-16 h-16"
                src={staticFile('/icons/message.png')}
              />
              <p className="whitespace-nowrap right-3 relative">
                {num_comments} comments
              </p>
            </div>
            <div className="flex items-center gap-4">
              <Img
                className="invert w-12 h-12"
                src={staticFile('/icons/gift.png')}
              />
              <p>Award</p>
            </div>
            <div className="flex items-center gap-4">
              <Img
                className="invert w-12 h-12"
                src={staticFile('/icons/right.png')}
              />
              <p>Share</p>
            </div>
            <div className="flex items-center gap-4">
              <Img
                className="invert w-12 h-12"
                src={staticFile('/icons/bookmark.png')}
              />
              <p>Save</p>
            </div>
            <div className="flex items-center gap-4">
              <Img
                className="invert w-12 h-12"
                src={staticFile('/icons/more.png')}
              />
            </div>
          </div>
        )}
      </div>
      <Audio src={staticFile(title_audio_file)} />
    </div>
  );
};

const Comment = ({
  beginning,
  author,
  time_ago,
  avatar_file,
  content,
  audio,
}) => {
  return (
    <div className="flex gap-6">
      {beginning ? (
        <Img className="rounded-full w-24 h-24" src={staticFile(avatar_file)} />
      ) : (
        <div className="w-24 flex-none" />
      )}
      <div className="flex gap-4 flex-col">
        {beginning && (
          <div className="flex gap-3 text-4xl">
            <p className="font-semibold">{author}</p>
            <p className="opacity-70">·</p>
            <p className="opacity-70">{time_ago}</p>
          </div>
        )}
        <p className="text-5xl">{content}</p>
      </div>
      <Audio src={staticFile(audio)} />
    </div>
  );
};

export const MyComposition = ({data, numberOfComments}) => {
  const post = useMemo(() => {
    const title = (
      <Series.Sequence
        durationInFrames={Math.ceil(
          Number(data.title_audio_file_lenght) * fps + BETWEEN
        )}
      >
        <Card>
          <Title
            first
            author={data.author}
            title={data.title}
            time_ago={data.time_ago}
            title_audio_file={data.title_audio_file}
            ups={data.ups}
            subreddit_name={data.subreddit_name}
            subreddit_logo_file={data.subreddit_logo_file}
            num_comments={data.num_comments}
            last={!data.selftext}
          />
        </Card>
      </Series.Sequence>
    );
    let selftext;
    if (data.selftext) {
      selftext = data.selftext.map((part, index) => {
        return (
          <Series.Sequence
            key={part.audio}
            durationInFrames={Math.ceil(Number(part.length) * fps + BETWEEN)}
          >
            <Card>
              <Title
                author={data.author}
                title={data.title}
                time_ago={data.time_ago}
                title_audio_file={part.audio}
                ups={data.ups}
                subreddit_name={data.subreddit_name}
                subreddit_logo_file={data.subreddit_logo_file}
                num_comments={data.num_comments}
                selftext={part.text}
                last={index === data.selftext.length - 1}
              />
            </Card>
          </Series.Sequence>
        );
      });
    }

    return (
      <>
        {title}
        {selftext}
      </>
    );
  }, [
    data.author,
    data.num_comments,
    data.selftext,
    data.subreddit_logo_file,
    data.subreddit_name,
    data.time_ago,
    data.title,
    data.title_audio_file,
    data.title_audio_file_lenght,
    data.ups,
  ]);

  const comments = useMemo(() => {
    return data.comments
      .map((comment) => {
        return comment.body.map((part, index) => {
          return (
            <Series.Sequence
              durationInFrames={Math.ceil(Number(part.length) * fps + BETWEEN)}
            >
              <Card>
                <Comment
                  beginning={index === 0}
                  author={comment.author}
                  time_ago={comment.time_ago}
                  ups={comment.ups}
                  avatar_file={comment.avatar_file}
                  content={part.text}
                  audio={part.audio}
                />
              </Card>
            </Series.Sequence>
          );
        });
      })
      .slice(0, numberOfComments);
  }, [data.comments, numberOfComments]);

  const videoFrom = Math.floor(
    random(data.title) * (SECONDS_IN_VIDEO - 61) * fps
  );

  return (
    <AbsoluteFill className="bg-gray-100 items-center justify-center text-zinc-50 text-4xl">
      <Series>
        {post}
        {comments}
      </Series>
      <OffthreadVideo
        src={staticFile('/bg.mp4')}
        volume={0}
        startFrom={videoFrom}
        className="absolute"
      />
      <Audio src={staticFile('/music/stal.mp3')} volume={0.05} />
    </AbsoluteFill>
  );
};
