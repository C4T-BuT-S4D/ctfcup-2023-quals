FROM openjdk:17-slim-bullseye

WORKDIR /app/
COPY twofac-demo/ .
RUN  ./gradlew --no-daemon build

ENTRYPOINT ["java", "-jar", "build/libs/twofac-demo-all.jar"]
