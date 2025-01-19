import React, { useState, useRef, useCallback, useEffect } from "react";
import { View, Image, StyleSheet, Text, Button } from "react-native";
import { useFocusEffect } from "@react-navigation/native";

export default function LiveVideoScreen() {
  const [liveFeed, setLiveFeed] = useState<string | null>(null); // Current frame
  const [isPaused, setIsPaused] = useState(false);
  const timeoutRef = useRef<number | null>(null);

  const API_GET_FRAMES_URL = "http://10.0.0.98:5000/api/get-frames";

  const fetchFrames = async () => {
    try {
      const response = await fetch(API_GET_FRAMES_URL);
      const data = await response.json();

      if (data.frames && data.frames.length > 0) {
        const lastFrame = data.frames[data.frames.length - 1];
        setLiveFeed(lastFrame);
      } else {
        setLiveFeed(null); // No frames available
      }
    } catch (error) {
      console.error("Error fetching frames:", error);
      setLiveFeed(null); // Reset on error
    }

    if (!isPaused) {
      timeoutRef.current = window.setTimeout(fetchFrames, 100);
    }
  };

  const startFetching = useCallback(() => {
    if (!timeoutRef.current) {
      fetchFrames();
    }
  }, [isPaused]);

  const stopFetching = useCallback(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      if (!isPaused) {
        startFetching();
      }

      return () => stopFetching();
    }, [isPaused, startFetching, stopFetching])
  );

  useEffect(() => {
    return () => stopFetching();
  }, [stopFetching]);

  return (
    <View style={styles.container}>
      <View style={styles.videoContainer}>
        {liveFeed ? (
          <Image
            source={{ uri: liveFeed }}
            style={styles.liveFeed}
            onError={() => console.error("Error rendering the image", liveFeed)}
          />
        ) : (
          <View style={styles.noVideoContainer}>
            <Text style={styles.noVideoText}>No Video Input</Text>
          </View>
        )}
      </View>
      <View style={styles.buttonContainer}>
        <Button
          title={isPaused ? "Resume" : "Pause"}
          onPress={() => {
            setIsPaused(!isPaused);
            if (isPaused) {
              startFetching();
            } else {
              stopFetching();
            }
          }}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#000",
  },
  videoContainer: {
    width: "90%",
    height: "70%",
    borderWidth: 2,
    borderColor: "#fff",
    borderRadius: 10,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#222",
  },
  liveFeed: {
    width: "100%",
    height: "100%",
    resizeMode: "contain",
  },
  noVideoContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  noVideoText: {
    color: "#fff",
    fontSize: 18,
    textAlign: "center",
  },
  buttonContainer: {
    marginTop: 20,
  },
});
