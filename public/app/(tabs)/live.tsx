import React, { useState, useEffect, useRef } from 'react';
import { View, Image, StyleSheet, Button } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';

import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';

export default function LiveScreen() {
  const [liveFeed, setLiveFeed] = useState<string | null>(null);
  const [isPaused, setIsPaused] = useState(false);

  const socketRef = useRef<WebSocket | null>(null);

  const WEBSOCKET_URL = 'http://10.0.0.98:5000';

  const startSocketConnection = () => {
    if (socketRef.current) {
      console.log('WebSocket already connected');
      return;
    }

    const socket = new WebSocket(WEBSOCKET_URL);
    socketRef.current = socket;

    socket.onopen = () => {
      console.log('WebSocket connected');
      socket.send(JSON.stringify({ type: 'request_frame' }));
    };

    socket.onmessage = (event) => {
      const blob = new Blob([event.data], { type: 'image/jpeg' });
      const objectUrl = URL.createObjectURL(blob);
      setLiveFeed(objectUrl);
    };

    socket.onclose = () => {
      console.log('WebSocket disconnected');
      socketRef.current = null;
    };

    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  };

  const stopSocketConnection = () => {
    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null;
      console.log('WebSocket connection closed');
    }
  };

  const handlePauseResume = () => {
    if (isPaused) {
      setIsPaused(false);
      startSocketConnection();
    } else {
      setIsPaused(true);
      stopSocketConnection();
    }
  };

  useFocusEffect(
    React.useCallback(() => {
      startSocketConnection();

      // Clean up when the screen loses focus
      return () => {
        stopSocketConnection();
      };
    }, []) // Dependency array ensures the effect is re-run only when the screen gains/loses focus
  );

  return (
    <ThemedView style={styles.container}>
      <View style={styles.liveFeedContainer}>
        {liveFeed ? (
          <Image source={{ uri: liveFeed }} style={styles.liveFeed} />
        ) : (
          <ThemedText type="subtitle">Loading live feed...</ThemedText>
        )}
      </View>

      {/* Pause/Resume Button */}
      <View style={styles.buttonContainer}>
        <Button title={isPaused ? 'Resume' : 'Pause'} onPress={handlePauseResume} />
      </View>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  liveFeedContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    marginVertical: 16,
  },
  liveFeed: {
    width: '100%',
    height: 200,
    resizeMode: 'contain',
  },
  buttonContainer: {
    marginVertical: 16,
  },
});
