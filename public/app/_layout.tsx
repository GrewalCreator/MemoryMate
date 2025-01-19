import React from 'react';
import { Stack } from 'expo-router';
import { AuthProvider, useAuth } from './auth/authContext';
import { ThemeProvider, DarkTheme, DefaultTheme } from '@react-navigation/native';
import { useColorScheme } from '../hooks/useColorScheme';
import { View, ActivityIndicator } from 'react-native';

export default function RootLayout() {
  return (
    <AuthProvider>
      <RootContent />
    </AuthProvider>
  );
}

function RootContent() {
  const { token } = useAuth();
  const colorScheme = useColorScheme();

  // Loading indicator if token is undefined
  if (token === undefined) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color="#000" />
      </View>
    );
  }

  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <Stack>
        {!token ? (
          <Stack.Screen name="pages/login" options={{ headerShown: false }} />
        ) : (
          <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        )}
      </Stack>
    </ThemeProvider>
  );
}
