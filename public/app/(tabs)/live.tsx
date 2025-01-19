import React, { useState, useRef, useCallback, useEffect } from "react";
import { View, Image, StyleSheet, Text, Button, Alert } from "react-native";
import { useFocusEffect } from "@react-navigation/native";

export default function LiveVideoScreen() {
  const [liveFeed, setLiveFeed] = useState<string | null>(null);
  const [isPaused, setIsPaused] = useState(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const API_GET_FRAMES_URL = "http://localhost:5000/api/stream";

  const fetchFrames = async () => {
    try {
      const response = await fetch(API_GET_FRAMES_URL, {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const text = await response.text();
      const data = text ? JSON.parse(text) : {};

      if (data.image_path) {
        console.log(data);
        console.log("Received image path:", data.image_path);
        const timestampedPath = `${data.image_path}?t=${new Date().getTime()}`;
        setLiveFeed(timestampedPath);
      } else {
        console.log("No new frame received.");
      }
    } catch (error) {
      console.error("Error fetching frames:", error);
    } finally {
      if (!isPaused) {
        timeoutRef.current = setTimeout(fetchFrames, 500);
      }
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
            setIsPaused((prev) => {
              const newPausedState = !prev;
              if (newPausedState) {
                stopFetching();
              } else {
                startFetching();
              }
              return newPausedState;
            });
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
