FROM mtr.devops.telekom.de/arthur_ferdinand_lindner/nginx:1.22-alpine

WORKDIR /usr/share/nginx/html

# Clean the default public folder
RUN rm -fr * .??*

# Finally, the "public" folder generated by Hugo in the previous stage
# is copied into the public fold of nginx
COPY /implementations /usr/share/nginx/html/implementations
COPY /index.html /usr/share/nginx/html/index.html
COPY /gitlab-safescarf.yml /usr/share/nginx/html/gitlab-safescarf.yml

COPY nginx.conf /etc/nginx/conf.d/default.conf
