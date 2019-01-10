# base image
FROM node:latest

# set working directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /usr/src/app/package.json
RUN npm i npm@latest -g
RUN npm install -g @angular/cli@latest
RUN npm i --package-lock-only
RUN npm audit fix

# add app
COPY . /usr/src/app

# start app
CMD ng serve --host 0.0.0.0 --public-host ltdemos.informatik.uni-hamburg.de
